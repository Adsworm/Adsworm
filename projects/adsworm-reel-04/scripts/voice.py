"""Dialogue audio (one ElevenLabs pass) → tightened voice.wav + word-timed timeline.json.

    python3 scripts/voice.py [script/dialogue-v1.mp3]

1. Cap every silence at GAP_CAP (how creators "jump-cut" breaths) and speed up by TEMPO (pitch kept).
2. Whisper word timestamps on the final audio, aligned to script/script.json words, so captions and
   camera beats land on the spoken word.
3. Per-frame loudness envelope (drives the orb and the avatar bounce).
"""
import datetime as dt
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
SR, FPS = 48000, 30
GAP_CAP, TAIL = 0.2, 0.5
TEMPO = float(os.environ.get("TEMPO", "1.06"))
# Spoken words → what the caption shows (applied to runs of consecutive words).
SHOW = {"eighteen point nine percent": "18.9%", "twenty": "20", "three things": "3 things", "three versions": "3 versions", "a thousand": "1,000", "seven": "7", "Advantage Plus": "Advantage+"}

model = WhisperModel("small", device="cpu", compute_type="int8")


def pcm(path: str, sr: int) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768


def words_of(x16: np.ndarray):
    segs, _ = model.transcribe(x16, language="en", word_timestamps=True, vad_filter=False)
    return [w for s in segs for w in s.words]


def tighten(src: str) -> np.ndarray:
    x = pcm(src, SR)
    ws = words_of(pcm(src, 16000))
    keep, cursor = [], 0
    for a, b in zip(ws, ws[1:]):
        gap = b.start - a.end
        if gap > GAP_CAP:
            cut_from = int((a.end + GAP_CAP / 2) * SR)
            cut_to = int((b.start - GAP_CAP / 2) * SR)
            keep.append((cursor, cut_from))
            cursor = cut_to
    keep.append((cursor, min(len(x), int((ws[-1].end + 0.15) * SR))))
    fade = int(0.012 * SR)
    out = []
    for s, e in keep:
        seg = x[max(0, s - fade if out else int(max(0, ws[0].start - 0.05) * SR)) : e].copy()
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        out.append(seg)
    return np.concatenate(out)


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "script/dialogue-v1.mp3")
    script = json.loads((ROOT / "script/script.json").read_text())
    y = tighten(src)
    tmp = ROOT / "public/voice/_tight.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(tmp)], input=y.tobytes(), check=True)
    out = ROOT / "public/voice.wav"
    pad = f"apad=pad_dur={TAIL}"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-af", f"highpass=f=70,atempo={TEMPO},{pad}", "-ar", str(SR), "-ac", "1", str(out)], check=True)
    tmp.unlink()

    final = pcm(str(out), 16000)
    heard = words_of(final)
    # script words, tagged with their line
    sw = [(i, w) for i, ln in enumerate(script["lines"]) for w in ln["say"].split()]
    hw = [norm(w.word) for w in heard]
    times: list = [None] * len(sw)
    sm = difflib.SequenceMatcher(a=[norm(w) for _, w in sw], b=hw, autojunk=False)
    for blk in sm.get_opcodes():
        tag, a0, a1, b0, b1 = blk
        if tag == "equal":
            for k in range(a1 - a0):
                times[a0 + k] = (heard[b0 + k].start, heard[b0 + k].end)
        elif tag == "replace" and b1 > b0:  # e.g. "eighteen point nine percent" ↔ "18 .9 %": spread the heard span
            s, e = heard[b0].start, heard[b1 - 1].end
            n = a1 - a0
            for k in range(n):
                times[a0 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
    # fill gaps by interpolation
    for k, t in enumerate(times):
        if t is None:
            prev = next((times[j][1] for j in range(k - 1, -1, -1) if times[j]), 0.0)
            nxt = next((times[j][0] for j in range(k + 1, len(times)) if times[j]), prev + 0.3)
            times[k] = (prev, max(prev + 0.05, nxt))
    missing = sum(1 for blk in sm.get_opcodes() if blk[0] != "equal")
    lines = []
    for i, ln in enumerate(script["lines"]):
        idx = [k for k, (li, _) in enumerate(sw) if li == i]
        raw = [{"w": sw[k][1], "s": round(times[k][0], 3), "e": round(times[k][1], 3)} for k in idx]
        # merge SHOW runs into one display token
        words, j = [], 0
        while j < len(raw):
            for key, show in SHOW.items():
                parts = key.split()
                cand = [norm(r["w"]) for r in raw[j : j + len(parts)]]
                if cand == [norm(p) for p in parts]:
                    tail = re.sub(r"^[\w']+", "", raw[j + len(parts) - 1]["w"].split()[-1])  # keep trailing punctuation
                    words.append({"w": show + re.sub(r"[\w%]", "", tail), "s": raw[j]["s"], "e": raw[j + len(parts) - 1]["e"]})
                    j += len(parts)
                    break
            else:
                words.append(raw[j])
                j += 1
        his = {norm(SHOW.get(h, h)) for phrase in ln.get("hi", []) for h in [phrase, *phrase.split()]}
        his |= {norm(t) for phrase in ln.get("hi", []) for t in SHOW.get(phrase, phrase).split()}
        for w in words:
            w["hi"] = norm(w["w"]) in his or any(norm(t) in his for t in w["w"].split())
        lines.append({"who": ln["who"], "room": ln["room"], "snap": ln.get("snap"), "start": words[0]["s"], "end": words[-1]["e"], "words": words})
    # rooms: from the first line of a room to the start of the next room
    rooms = []
    for ln in lines:
        if not rooms or rooms[-1]["id"] != ln["room"]:
            rooms.append({"id": ln["room"], "start": ln["start"]})
    dur = len(final) / 16000
    for a, b in zip(rooms, rooms[1:] + [{"start": dur}]):
        a["end"] = b["start"]
    # loudness envelope per frame (0..1)
    x = pcm(str(out), SR)
    hop = SR // FPS
    rms = np.array([np.sqrt(np.mean(x[i : i + hop] ** 2)) for i in range(0, len(x), hop)])
    env = np.clip(rms / (np.percentile(rms, 95) + 1e-6), 0, 1)
    cd = script.get("vars", {}).get("countdown")
    days = int(os.environ.get("REEL_DAYS") or (dt.date.fromisoformat(cd["to"]) - dt.date.today()).days) if cd else None
    tl = {
        "fps": FPS,
        "durationInFrames": int(np.ceil(dur * FPS)),
        "lines": lines,
        "rooms": rooms,
        "env": [round(float(v), 2) for v in env],
        "vars": {"days": days, "countdownLabel": cd.get("label") if cd else ""},
    }
    (ROOT / "src/reel/timeline.json").write_text(json.dumps(tl, ensure_ascii=False))
    gaps = [b.start - a.end for a, b in zip(heard, heard[1:])]
    print(f"voice.wav {dur:.1f}s · {len(heard) / (heard[-1].end - heard[0].start):.2f} words/s · max gap {max(gaps):.2f}s · unaligned blocks {missing}")
    for ln in lines:
        print(f"  {ln['start']:5.2f}-{ln['end']:5.2f} {ln['who']:4} {' '.join(('*' if w['hi'] else '') + w['w'] for w in ln['words'])}")


if __name__ == "__main__":
    main()

"""Voice + timeline engine (one-pass dialogue).

script/dialogue.mp3 (the whole conversation, ONE ElevenLabs v4 call — see README)
script/script.json  →  public/voice.wav (voice + soft bed + UI pops)  +  src/reel/timeline.json

1. Silences longer than `gapCap` are cut down (how creators jump-cut breaths); no per-line TTS, so
   nothing sounds stitched.
2. Whisper word timestamps on the tightened audio, aligned to the script's `say` words → each line's
   start/end. [brackets] in `show` become highlight pills; a line's `beat` builds its card element the
   moment the line starts, so picture, caption and voice share one clock.

    python3 scripts/voice.py              # REEL_DAYS=n forces the countdown on the hook card
"""
import difflib
import json
import os
import re
import subprocess
import sys
import wave
from datetime import date
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "script/script.json"
SRC = ROOT / "script/dialogue.mp3"
SR, FPS = 48000, 30
rng = np.random.default_rng(3)
model = WhisperModel("small", device="cpu", compute_type="int8")


def countdown(s):
    cd = s.get("vars", {}).get("countdown")
    if not cd:
        return {}
    days = int(os.environ["REEL_DAYS"]) if os.environ.get("REEL_DAYS") else (date.fromisoformat(cd["to"]) - date.today()).days
    if days <= 0:
        print(f"WARNING: countdown to {cd['to']} is {days} days — the hook no longer holds", file=sys.stderr)
    return {"days": days}


def pills(show: str):
    """'[6 saal] se Meta ads' → text without brackets + list of highlighted spans (by word index)."""
    words, spans, i = [], [], 0
    for tok in re.findall(r"\[[^\]]+\]\S*|\S+", show):
        if tok.startswith("["):
            close = tok.index("]")
            inner = tok[1:close].split()
            inner[-1] += tok[close + 1:]  # trailing punctuation rides on the last word, outside the pill
            spans.append([i, i + len(inner)])
            words += inner
            i += len(inner)
        else:
            words.append(tok)
            i += 1
    return " ".join(words), spans


def pcm(path, sr):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768


def heard(x16):
    segs, _ = model.transcribe(x16.astype(np.float32), language="en", word_timestamps=True)
    return [w for s in segs for w in s.words]


def tighten(x, ws, cap):
    """Keep speech, shorten every pause to `cap` seconds (12 ms crossfades)."""
    keep, cursor = [], int(max(0, ws[0].start - 0.05) * SR)
    for a, b in zip(ws, ws[1:]):
        if b.start - a.end > cap:
            keep.append((cursor, int((a.end + cap / 2) * SR)))
            cursor = int((b.start - cap / 2) * SR)
    keep.append((cursor, min(len(x), int((ws[-1].end + 0.2) * SR))))
    f = int(0.012 * SR)
    out = []
    for s, e in keep:
        seg = x[s:e].copy()
        seg[:f] *= np.linspace(0, 1, f)
        seg[-f:] *= np.linspace(1, 0, f)
        out.append(seg)
    return np.concatenate(out)


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def lp(x, hz):
    return sosfilt(butter(2, hz, "low", fs=SR, output="sos"), x)


def pop(freq=520):
    t = np.arange(int(0.09 * SR)) / SR
    f = freq * 0.7 + freq * 1.2 * np.exp(-t * 55)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40) * 0.5


def whoosh(dur=0.35):
    t = np.arange(int(dur * SR)) / SR
    return lp(rng.standard_normal(len(t)), 2200) * np.sin(np.pi * t / dur) ** 2 * 0.25


def bed(dur):
    """Soft, beatless pad far under the voice."""
    t = np.arange(int(dur * SR)) / SR
    x = np.zeros_like(t)
    for f, g in ((110.0, 1.0), (164.81, 0.6), (220.0, 0.5), (261.63, 0.35)):
        x += np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.07 * t)) * g
    x = lp(x / 2.5, 900)
    return x * (0.85 + 0.15 * np.sin(2 * np.pi * t / 11)) * np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)


def place(track, clip, at_s, gain=1.0):
    i = int(at_s * SR)
    j = min(len(track), i + len(clip))
    if 0 <= i < len(track):
        track[i:j] += clip[: j - i] * gain


def main():
    s = json.loads(SCRIPT.read_text())
    vars_ = countdown(s)
    flat = [(sec, ln) for sec in s["sections"] for ln in sec["lines"]]
    lead = s.get("leadInMs", 120) / 1000

    raw = pcm(SRC, SR)
    voice = tighten(raw, heard(pcm(SRC, 16000)), s.get("gapCap", 0.26))
    tempo = s.get("tempo", 1.0)
    if tempo != 1.0:
        voice = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo}", "-f", "f64le", "-"], input=voice.tobytes(), capture_output=True, check=True).stdout)
    voice = np.concatenate([np.zeros(int(lead * SR)), voice])

    # word timings on the final voice, aligned to the script
    x16 = np.interp(np.arange(0, len(voice), SR / 16000), np.arange(len(voice)), voice)
    hw = heard(x16)
    sw = [(k, w) for k, (_, ln) in enumerate(flat) for w in ln["say"].split()]
    times = [None] * len(sw)
    for tag, a0, a1, b0, b1 in difflib.SequenceMatcher(a=[norm(w) for _, w in sw], b=[norm(w.word) for w in hw], autojunk=False).get_opcodes():
        if tag == "equal":
            for i in range(a1 - a0):
                times[a0 + i] = (hw[b0 + i].start, hw[b0 + i].end)
        elif tag == "replace" and b1 > b0:
            st, en = hw[b0].start, hw[b1 - 1].end
            for i in range(a1 - a0):
                times[a0 + i] = (st + (en - st) * i / (a1 - a0), st + (en - st) * (i + 1) / (a1 - a0))
    for i, t in enumerate(times):
        if t is None:
            prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
            nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev + 0.3)
            times[i] = (prev, max(prev + 0.05, nxt))

    lines, sections = [], []
    for k, (sec, ln) in enumerate(flat):
        idx = [i for i, (kk, _) in enumerate(sw) if kk == k]
        show, spans = pills(ln["show"])
        lines.append({
            "n": k + 1, "section": sec["id"], "who": ln["who"], "show": show, "pills": spans,
            "beat": ln.get("beat"), "pose": ln.get("pose"),
            "start": round(times[idx[0]][0], 3), "end": round(times[idx[-1]][1], 3),
            "words": [{"t": round(times[i][0], 3), "d": round(times[i][1] - times[i][0], 3), "w": sw[i][1]} for i in idx],
        })
    for sec in s["sections"]:
        ls = [l for l in lines if l["section"] == sec["id"]]
        sections.append({"id": sec["id"], "label": sec.get("label", ""), "tag": sec.get("tag", ""), "source": sec.get("source", ""), "start": ls[0]["start"], "end": ls[-1]["end"], "views": sec.get("views", [])})
    total = len(voice) / SR + s.get("tailMs", 1200) / 1000
    frames = int(np.ceil(total * FPS))

    track = np.zeros(int(total * SR))
    track[: len(voice)] = voice
    fx = np.zeros_like(track)
    beats = {}
    for ln in lines:
        if ln["beat"]:
            beats[ln["beat"]] = int(round(ln["start"] * FPS))
            place(fx, pop(480 + 40 * (len(beats) % 5)), ln["start"] + 0.12, 0.7)
    if lines and lines[0]["beat"]:
        beats[lines[0]["beat"]] = -24  # the hook visual is the thumbnail: already landed on frame 0
    for sec in sections[1:]:
        place(fx, whoosh(), sec["start"] - 0.2, 0.8)
    mix = track * 0.95 + bed(total) * s.get("bedGain", 0.08) + fx * s.get("fxGain", 1.0)
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix /= max(1e-9, np.max(np.abs(mix))) / 0.9
    with wave.open(str(ROOT / "public/voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())

    tl = {"fps": FPS, "variant": "organic", "vars": vars_, "durationInFrames": frames, "voices": s["voices"], "brand": s.get("brand", {}), "lines": lines, "sections": sections, "beats": beats}
    (ROOT / "src/reel/timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    gaps = [b.start - a.end for a, b in zip(hw, hw[1:])]
    print(f"{len(lines)} lines · {total:.1f}s · {len(hw) / (hw[-1].end - hw[0].start):.2f} words/s · max gap {max(gaps):.2f}s → public/voice.wav, src/reel/timeline.json")
    for ln in lines:
        print(f"  {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['who']:<5} {ln['show'][:70]}")


if __name__ == "__main__":
    main()

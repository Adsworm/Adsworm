"""Voice + timeline engine (one-pass dialogue).

script/dialogue.mp3 (the whole conversation, ONE ElevenLabs v4 call — `python3 scripts/dialogue.py`
prints the request) + script/script.json  →  public/voice.wav (voice + ducked pad)  +  src/reel/timeline.json

1. Quiet pauses longer than `gapCap` are cut down (how creators jump-cut breaths); laughs and gasps from
   audio tags are kept. No per-line TTS, so nothing sounds stitched.
2. Whisper word timestamps on the tightened audio, aligned to the script's `say` words → each line's
   start/end and every caption token's time. [brackets] in `show` become highlight pills.
3. `payoff` opens a held breath before the line that answers the hook; `loop` rides along to the engine.
Sound effects are not mixed here: the visuals play their own (src/reel/Sfx.tsx).

    REEL=<slug> python3 scripts/voice.py                              # REEL_DAYS=n forces the countdown
    REEL=<slug> DIALOGUE=dialogue.draft.mp3 python3 scripts/voice.py   # free draft voice (scripts/draft_voice.py)
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
# One engine, many reels: REEL=<slug> works on reels/<slug>/ (script.json, dialogue.mp3, sources.md).
DIR = ROOT / "reels" / os.environ["REEL"] if os.environ.get("REEL") else ROOT / "script"
SCRIPT = DIR / "script.json"
SRC = DIR / os.environ.get("DIALOGUE", "dialogue.mp3")
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
    """Keep speech, shorten every QUIET pause to `cap` seconds (12 ms crossfades). Gaps that hold sound
    Whisper doesn't transcribe (a laugh, a gasp from an audio tag) are kept."""
    keep, cursor = [], int(max(0, ws[0].start - 0.05) * SR)
    floor = np.sqrt(np.mean(x ** 2)) * 0.25
    for a, b in zip(ws, ws[1:]):
        seg = x[int(a.end * SR) : int(b.start * SR)]
        quiet = len(seg) == 0 or np.sqrt(np.mean(seg ** 2)) < floor
        if b.start - a.end > cap and quiet:
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


def tokens_for(show, spans, said):
    """Karaoke timing for caption tokens: an exact word match takes that word's time; anything else
    (\"59%\" for \"fifty-nine percent\") is placed proportionally between its neighbours."""
    toks = show.split(" ")
    pill = [any(a <= i < b for a, b in spans) for i in range(len(toks))]
    out, j = [], 0
    for i, tok in enumerate(toks):
        t = None
        for k in range(j, min(j + 4, len(said))):
            if norm(said[k][0]) == norm(tok) and norm(tok):
                t, j = said[k][1], k + 1
                break
        if t is None:
            k = min(len(said) - 1, round(i * (len(said) - 1) / max(1, len(toks) - 1)))
            t = said[max(k, min(j, len(said) - 1))][1]
        out.append({"w": tok, "t": round(t, 3), "pill": pill[i]})
    for a, b in zip(out, out[1:]):  # keep times monotonic
        b["t"] = max(b["t"], a["t"])
    return out


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


def thump(dur=0.45):
    t = np.arange(int(dur * SR)) / SR
    f = 48 + 90 * np.exp(-t * 28)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) + rng.standard_normal(len(t)) * np.exp(-t * 220) * 0.3) * 0.8


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

    # Payoff: a held breath before the line that answers the hook. The engine plays a riser into it and
    # a bass hit as it lands (Reel.tsx); here we open the gap and move every later timing by its length.
    payoff, payoff_tl = s.get("payoff"), None
    if payoff:
        k = next(i for i, (_, ln) in enumerate(flat) if ln.get("beat") == payoff["beat"])
        first = next(i for i, (kk, _) in enumerate(sw) if kk == k)
        pause = payoff.get("pauseMs", 350) / 1000
        at = max(0.0, times[first][0] - 0.05)
        cut, f = int(at * SR), int(0.008 * SR)
        head, tail = voice[:cut].copy(), voice[cut:].copy()
        head[-f:] *= np.linspace(1, 0, f)
        tail[:f] *= np.linspace(0, 1, f)
        voice = np.concatenate([head, np.zeros(int(pause * SR)), tail])
        times = [(a + pause, b + pause) if a >= at - 1e-6 else (a, b) for a, b in times]
        payoff_tl = {"beat": payoff["beat"], "frame": int(round((at + pause + 0.05) * FPS)), "pauseFrames": int(round(pause * FPS)), "silence": [at, at + pause]}

    lines, sections = [], []
    for k, (sec, ln) in enumerate(flat):
        idx = [i for i, (kk, _) in enumerate(sw) if kk == k]
        show, spans = pills(ln["show"])
        lines.append({
            "n": k + 1, "section": sec["id"], "who": ln["who"], "show": show, "pills": spans,
            "beat": ln.get("beat"), "pose": ln.get("pose"),
            # acting: `pre` = the speaker's face in the beat before the line (the laugh/gasp from its audio
            # tag), `react` = the listener's face during the line (from `reactWord`, if given)
            "pre": ln.get("pre"), "react": ln.get("react"), "reactWord": ln.get("reactWord"),
            "start": round(times[idx[0]][0], 3), "end": round(times[idx[-1]][1], 3),
            "words": [{"t": round(times[i][0], 3), "d": round(times[i][1] - times[i][0], 3), "w": sw[i][1]} for i in idx],
            "tokens": tokens_for(show, spans, [(sw[i][1], times[i][0]) for i in idx]),
        })
    for sec in s["sections"]:
        ls = [l for l in lines if l["section"] == sec["id"]]
        sections.append({"id": sec["id"], "label": sec.get("label", ""), "tag": sec.get("tag", ""), "source": sec.get("source", ""), "start": ls[0]["start"], "end": ls[-1]["end"], "views": sec.get("views", [])})
    total = len(voice) / SR + s.get("tailMs", 1200) / 1000
    frames = int(np.ceil(total * FPS))

    track = np.zeros(int(total * SR))
    track[: len(voice)] = voice
    beats = {ln["beat"]: int(round(ln["start"] * FPS)) for ln in lines if ln["beat"]}
    # Effects are not mixed here any more: each visual plays its own (src/reel/Sfx.tsx), so sound
    # can't drift from picture. This file is voice + the quiet pad only.
    # The pad ducks under the voice (commentary should sit ≥ 15 LU over its bed) and drops out for the
    # payoff's held breath.
    duck = lp(np.abs(track), 6)
    duck = np.clip(duck / (np.percentile(duck, 95) + 1e-9), 0, 1)
    pad = bed(total) * (1 - 0.6 * duck)
    if payoff_tl:
        a, b = (int(v * SR) for v in payoff_tl["silence"])
        g = np.ones(len(pad))
        f = int(0.03 * SR)
        g[a:b] = 0
        g[max(0, a - f) : a] = np.linspace(1, 0, min(f, a))
        g[b : b + f] = np.linspace(0, 1, len(g[b : b + f]))
        pad *= g
    mix = track * 0.95 + pad * s.get("bedGain", 0.08)
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix /= max(1e-9, np.max(np.abs(mix))) / 0.9
    with wave.open(str(ROOT / "public/voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())

    hop = SR // FPS
    rms = np.array([np.sqrt(np.mean(track[i : i + hop] ** 2)) for i in range(0, len(track), hop)])
    env = np.clip(rms / (np.percentile(rms[rms > 1e-4], 90) + 1e-9), 0, 1)
    tl = {"env": [round(float(v), 2) for v in env], "fps": FPS, "variant": "organic", "vars": vars_, "durationInFrames": frames, "voices": s["voices"], "brand": s.get("brand", {}), "loop": s.get("loop"), "payoff": payoff_tl, "lines": lines, "sections": sections, "beats": beats}
    (ROOT / "src/reel/timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    gaps = [b.start - a.end for a, b in zip(hw, hw[1:])]
    print(f"{len(lines)} lines · {total:.1f}s · {len(hw) / (hw[-1].end - hw[0].start):.2f} words/s · max gap {max(gaps):.2f}s → public/voice.wav, src/reel/timeline.json")
    for ln in lines:
        print(f"  {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['who']:<5} {ln['show'][:70]}")


if __name__ == "__main__":
    main()

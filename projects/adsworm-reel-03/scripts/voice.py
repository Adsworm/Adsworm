"""Voice + timeline engine for the explainer module.

script/script.json  →  public/voice.wav (voice + soft bed + UI pops)  +  src/reel/timeline.json

Each script line has `say` (what the TTS reads — Devanagari for Hindi words so pronunciation is
right) and `show` (the Latin-script Hinglish caption). [brackets] in `show` become highlight
pills. A line's optional `beat` names the card element that builds the moment the line starts,
so picture, caption and voice can't drift: they all come from the same word timings.

    python3 scripts/voice.py            # synthesize everything
    python3 scripts/voice.py --no-tts   # rebuild timeline/mix from cached line audio
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import edge_tts
import numpy as np
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "script/script.json"
CACHE = ROOT / "public/voice"
SR = 48000
FPS = 30
PROXY = os.environ.get("HTTPS_PROXY")
rng = np.random.default_rng(3)


def pills(show: str):
    """'[6 saal] se Meta ads' → text without brackets + list of highlighted spans (by word index)."""
    words, spans, i = [], [], 0
    for tok in re.findall(r"\[[^\]]+\]|\S+", show):
        if tok.startswith("["):
            inner = tok[1:-1].split()
            spans.append([i, i + len(inner)])
            words += inner
            i += len(inner)
        else:
            words.append(tok)
            i += 1
    return " ".join(words), spans


async def tts(text: str, voice: str, rate: str, out: Path):
    com = edge_tts.Communicate(text, voice, rate=rate, proxy=PROXY, boundary="WordBoundary")
    audio, words = bytearray(), []
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            words.append({"t": round(ch["offset"] / 1e7, 3), "d": round(ch["duration"] / 1e7, 3), "w": ch["text"]})
    out.with_suffix(".mp3").write_bytes(audio)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out.with_suffix(".mp3")), "-ar", str(SR), "-ac", "1", str(out)], check=True)
    return words


def read_wav(p: Path):
    with wave.open(str(p)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
    return x


def lp(x, hz):
    return sosfilt(butter(2, hz, "low", fs=SR, output="sos"), x)


def pop(freq=520):
    t = np.arange(int(0.09 * SR)) / SR
    f = freq * 0.7 + freq * 1.2 * np.exp(-t * 55)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 40) * 0.5


def whoosh(dur=0.35):
    t = np.arange(int(dur * SR)) / SR
    n = rng.standard_normal(len(t))
    return lp(n, 2200) * np.sin(np.pi * t / dur) ** 2 * 0.25


def bed(dur):
    """Soft, beatless pad (A minor drone with slow movement) — sits far under the voice."""
    t = np.arange(int(dur * SR)) / SR
    x = np.zeros_like(t)
    for f, g in ((110.0, 1.0), (164.81, 0.6), (220.0, 0.5), (261.63, 0.35)):
        x += np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.07 * t)) * g
    x = lp(x / 2.5, 900)
    swell = 0.85 + 0.15 * np.sin(2 * np.pi * t / 11)
    fade = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
    return x * swell * fade


def place(track, clip, at_s, gain=1.0):
    i = int(at_s * SR)
    j = min(len(track), i + len(clip))
    if i < len(track):
        track[i:j] += clip[: j - i] * gain


def main(no_tts=False):
    s = json.loads(SCRIPT.read_text())
    CACHE.mkdir(parents=True, exist_ok=True)
    gap, sgap = s.get("gapMs", 220) / 1000, s.get("sectionGapMs", 450) / 1000
    lead = s.get("leadInMs", 150) / 1000
    cursor = lead
    lines, sections = [], []
    n = 0
    for sec in s["sections"]:
        sec_start = cursor
        for ln in sec["lines"]:
            n += 1
            wav = CACHE / f"{n:02d}.wav"
            meta = CACHE / f"{n:02d}.json"
            if not no_tts or not wav.exists():
                rate = s.get("rates", {}).get(ln["who"], s.get("rate", "+30%"))  # ~3 words/s matches the reference pace
                words = asyncio.run(tts(ln["say"], s["voices"][ln["who"]], rate, wav))
                meta.write_text(json.dumps(words, ensure_ascii=False))
            words = json.loads(meta.read_text())
            dur = len(read_wav(wav)) / SR
            show, spans = pills(ln["show"])
            lines.append({
                "n": n, "section": sec["id"], "who": ln["who"], "show": show, "pills": spans,
                "beat": ln.get("beat"), "pose": ln.get("pose"), "start": round(cursor, 3), "end": round(cursor + dur, 3),
                "words": [{"t": round(cursor + w["t"], 3), "d": w["d"], "w": w["w"]} for w in words],
            })
            cursor += dur + gap
        sections.append({"id": sec["id"], "label": sec.get("label", ""), "tag": sec.get("tag", ""), "source": sec.get("source", ""), "start": round(sec_start, 3), "end": round(cursor - gap, 3)})
        cursor += sgap - gap
    total = cursor + s.get("tailMs", 1200) / 1000
    frames = int(np.ceil(total * FPS))

    # mix: voice (mono→center) + bed + a pop on every beat, a whoosh on every section start
    voice = np.zeros(int(total * SR))
    for ln in lines:
        place(voice, read_wav(CACHE / f"{ln['n']:02d}.wav"), ln["start"])
    fx = np.zeros_like(voice)
    beats = {}
    for ln in lines:
        if ln["beat"]:
            beats[ln["beat"]] = int(round(ln["start"] * FPS))
            place(fx, pop(480 + 40 * (len(beats) % 5)), ln["start"] + 0.12, 0.7)  # lands with the element's settle
    if lines and lines[0]["beat"]:
        beats[lines[0]["beat"]] = -24  # the hook visual is the thumbnail: already landed on frame 0
    for sec in sections[1:]:
        place(fx, whoosh(), sec["start"] - 0.2, 0.8)
    mix = voice * 0.95 + bed(total) * 0.08 + fx
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix /= max(1e-9, np.max(np.abs(mix))) / 0.9
    out = ROOT / "public/voice.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())

    tl = {"fps": FPS, "durationInFrames": frames, "voices": s["voices"], "brand": s.get("brand", {}), "lines": lines, "sections": sections, "beats": beats}
    (ROOT / "src/reel/timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))
    print(f"{len(lines)} lines · {len(sections)} sections · {total:.1f}s · {frames} frames · {len(beats)} beats → public/voice.wav, src/reel/timeline.json")
    for ln in lines:
        print(f"  {ln['start']:6.2f}  {ln['who']:<8} {ln['show'][:70]}")


if __name__ == "__main__":
    main(no_tts="--no-tts" in sys.argv)

"""Free draft voice (edge-tts) → reels/<slug>/dialogue.draft.mp3, for layout and timing checks before
any credits are spent on the real ElevenLabs dialogue. Not for publishing: per-line TTS sounds stitched.

    REEL=<slug> python3 scripts/draft_voice.py && REEL=<slug> DIALOGUE=dialogue.draft.mp3 python3 scripts/voice.py
"""
import asyncio
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "reels" / os.environ["REEL"] if os.environ.get("REEL") else ROOT / "script"
VOICES = {
    "en": {"AMAN": "en-IN-PrabhatNeural", "RIYA": "en-IN-NeerjaExpressiveNeural"},
    "hi": {"AMAN": "hi-IN-MadhurNeural", "RIYA": "hi-IN-SwaraNeural"},  # Hinglish: Devanagari + English in `say`
}
PROXY = os.environ.get("HTTPS_PROXY")


RATE = os.environ.get("RATE", "+12%")


def letters(w):
    return re.sub(r"[\W_]+", "", w, flags=re.UNICODE).lower()


def per_word(text, bounds):
    """One (start, end) per script word from the engine's word boundaries. They usually match one to one;
    when the engine splits or joins a token (a hyphenated word, a number), boundaries are consumed by length."""
    words = text.split()
    if len(bounds) == len(words):
        return [(a, b) for _, a, b in bounds]
    out, k = [], 0
    for w in words:
        need, got, start, end = len(letters(w)), 0, None, None
        while k < len(bounds) and (start is None or got < need):
            tok, a, b = bounds[k]
            start = a if start is None else start
            end, got, k = b, got + max(1, len(letters(tok))), k + 1
        if start is None:  # ran out: reuse the last moment rather than fail a draft
            start = end = out[-1][1] if out else 0.0
        out.append((start, end))
    return out


async def say(text, voice, out):
    for attempt in range(4):  # the free endpoint sometimes returns no audio; a retry fixes it
        try:
            audio, bounds = b"", []
            async for ch in edge_tts.Communicate(text, voice, rate=RATE, proxy=PROXY, boundary="WordBoundary").stream():
                if ch["type"] == "audio":
                    audio += ch["data"]
                elif ch["type"] == "WordBoundary":
                    bounds.append((ch["text"], ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7))
            if not audio:
                raise edge_tts.exceptions.NoAudioReceived("empty")
            out.write_bytes(audio)
            return bounds
        except edge_tts.exceptions.NoAudioReceived:
            if attempt == 3:
                raise
            await asyncio.sleep(2 * (attempt + 1))


def main():
    s = json.loads((DIR / "script.json").read_text())
    lines = [ln for sec in s["sections"] for ln in sec["lines"]]
    voices = VOICES.get(s.get("lang", "en"), VOICES["en"])
    with tempfile.TemporaryDirectory() as d:
        parts, bounds = [], []
        for i, ln in enumerate(lines):
            p = Path(d) / f"{i:02d}.mp3"
            bounds.append(asyncio.run(say(ln["say"], voices[ln["who"]], p)))
            w = p.with_suffix(".wav")  # decode first: lengths of decoded parts add up exactly, mp3 frames do not
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-ar", "48000", "-ac", "1", str(w)], check=True)
            parts.append(w)
        # per-line start times: ground truth for checking the word aligner (scripts/align_check.py)
        durs = [float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(q)], capture_output=True, text=True).stdout) for q in parts]
        starts = [round(sum(durs[:i]), 3) for i in range(len(durs))]
        (DIR / "dialogue.draft.json").write_text(json.dumps({"starts": starts}))
        # exact word times (the engine reports them): voice.py reads <audio>.words.json and skips speech recognition
        words = [{"w": w, "start": round(starts[i] + a, 3), "end": round(starts[i] + b, 3)}
                 for i, ln in enumerate(lines) for w, (a, b) in zip(ln["say"].split(), per_word(ln["say"], bounds[i]))]
        (DIR / "dialogue.draft.words.json").write_text(json.dumps(words, ensure_ascii=False))
        lst = Path(d) / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        out = DIR / "dialogue.draft.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "48000", "-ac", "1", str(out)], check=True)
    print(f"{len(lines)} lines → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

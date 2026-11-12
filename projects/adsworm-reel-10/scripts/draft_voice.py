"""Free draft voice (edge-tts) → reels/<slug>/dialogue.draft.mp3, for layout and timing checks before
any credits are spent on the real ElevenLabs dialogue. Not for publishing: per-line TTS sounds stitched.

    REEL=<slug> python3 scripts/draft_voice.py && REEL=<slug> DIALOGUE=dialogue.draft.mp3 python3 scripts/voice.py
"""
import asyncio
import json
import os
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


async def say(text, voice, out):
    for attempt in range(4):  # the free endpoint sometimes returns no audio; a retry fixes it
        try:
            await edge_tts.Communicate(text, voice, rate="+12%", proxy=PROXY).save(str(out))
            return
        except edge_tts.exceptions.NoAudioReceived:
            if attempt == 3:
                raise
            await asyncio.sleep(2 * (attempt + 1))


def main():
    s = json.loads((DIR / "script.json").read_text())
    lines = [ln for sec in s["sections"] for ln in sec["lines"]]
    voices = VOICES.get(s.get("lang", "en"), VOICES["en"])
    with tempfile.TemporaryDirectory() as d:
        parts = []
        for i, ln in enumerate(lines):
            p = Path(d) / f"{i:02d}.mp3"
            asyncio.run(say(ln["say"], voices[ln["who"]], p))
            parts.append(p)
        # per-line start times: ground truth for checking the word aligner (scripts/align_check.py)
        durs = [float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(q)], capture_output=True, text=True).stdout) for q in parts]
        (DIR / "dialogue.draft.json").write_text(json.dumps({"starts": [round(sum(durs[:i]), 3) for i in range(len(durs))]}))
        lst = Path(d) / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        out = DIR / "dialogue.draft.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "48000", "-ac", "1", str(out)], check=True)
    print(f"{len(lines)} lines → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

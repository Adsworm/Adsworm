"""Print the Higgsfield generate_audio params for a reel's script (ONE ElevenLabs v4 dialogue call).
A line's optional `tags` (e.g. "[excited]") are prepended for the voice only; captions/timing use `say`.

    REEL=<slug> python3 scripts/dialogue.py      # save the generated audio as reels/<slug>/dialogue.mp3
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "reels" / os.environ["REEL"] if os.environ.get("REEL") else ROOT / "script"
s = json.loads((DIR / "script.json").read_text())
lines = [ln for sec in s["sections"] for ln in sec["lines"]]
print(json.dumps({"model": "elevenlabs_v4", "prompt": s.get("direction", "Natural, lively explainer dialogue."), "dialogue": [{"text": (ln.get("tags", "") + " " + ln["say"]).strip(), "voice_type": "preset", "voice_id": s["voices"][ln["who"]]["voice_id"]} for ln in lines]}, ensure_ascii=False))

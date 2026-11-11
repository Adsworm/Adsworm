"""Print the Higgsfield generate_audio params for script/script.json (ONE ElevenLabs v4 dialogue call).
A line's optional `tags` (e.g. "[excited]") are prepended for the voice only; captions/timing use `say`."""
import json
from pathlib import Path

s = json.loads((Path(__file__).resolve().parent.parent / "script/script.json").read_text())
lines = [ln for sec in s["sections"] for ln in sec["lines"]]
print(json.dumps({"model": "elevenlabs_v4", "prompt": s.get("direction", "Natural, lively explainer dialogue."), "dialogue": [{"text": (ln.get("tags", "") + " " + ln["say"]).strip(), "voice_type": "preset", "voice_id": s["voices"][ln["who"]]["voice_id"]} for ln in lines]}))

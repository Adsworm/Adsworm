"""Print the Higgsfield generate_audio params for a reel's script (ONE ElevenLabs v4 dialogue call).
A line's optional `tags` (e.g. "[excited]") are prepended for the voice only; captions/timing use `say`.
A line's optional `tts` replaces `say` for the voice engine only (same word count): Hinglish lines are sent
all in Devanagari ("ads" → "ऐड्स") so an English-trained voice does not flip into English pronunciation mid-sentence.

    REEL=<slug> python3 scripts/dialogue.py      # save the generated audio as reels/<slug>/dialogue.mp3
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "reels" / os.environ["REEL"] if os.environ.get("REEL") else ROOT / "script"
s = json.loads((DIR / "script.json").read_text())
# One turn per run of lines by the same speaker inside a section (unless a line carries its own audio tag):
# a sentence that spans two caption lines is voiced as one sentence.
turns = []
for sec in s["sections"]:
    for ln in sec["lines"]:
        text = ln.get("tts") or ln["say"]
        same = turns and turns[-1]["sec"] == sec["id"] and turns[-1]["who"] == ln["who"] and not ln.get("tags")
        if same:
            turns[-1]["text"] += " " + text
        else:
            turns.append({"sec": sec["id"], "who": ln["who"], "text": (ln.get("tags", "") + " " + text).strip()})
voice = lambda who: s["voices"][who]
print(json.dumps({"model": "elevenlabs_v4", "prompt": s.get("direction", "Natural, lively explainer dialogue."), "dialogue": [{"text": t["text"], "voice_type": voice(t["who"]).get("voice_type", "preset"), "voice_id": voice(t["who"])["voice_id"]} for t in turns]}, ensure_ascii=False))

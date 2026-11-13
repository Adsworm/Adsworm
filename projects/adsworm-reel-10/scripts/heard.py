"""Transcript check: print what speech recognition hears in a reel's voice file, next to the script.
I cannot listen; this is the evidence that every line was spoken and can be made out.

    REEL=<slug> python3 scripts/heard.py            # reads reels/<slug>/dialogue.mp3 (or DIALOGUE=<file>)
"""
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("voice", ROOT / "scripts" / "voice.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
s = json.loads(v.SCRIPT.read_text())
v.LANG = s.get("lang", "en")
words = v.heard(v.pcm(v.SRC, 16000))
text = " ".join(w.word.strip() for w in words)
(ROOT / "out").mkdir(exist_ok=True)
(ROOT / "out" / f"heard-{v.DIR.name}.txt").write_text(text + "\n")
script = [w for sec in s["sections"] for ln in sec["lines"] for w in (ln.get("tts") or ln["say"]).split()]
pairs = v.fuzzy_align(script, [w.word for w in words]) if v.LANG != "en" else []
print(text)
if pairs:
    print(f"\n{len(pairs)}/{len(script)} script words found by sound")

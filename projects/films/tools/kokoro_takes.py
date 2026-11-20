"""Narration takes with Kokoro (Apache-2.0), one WAV per take, a clear pause between lines.
usage: kokoro_takes.py PROJECT VOICE SPEED OUT_DIR"""
import json, pathlib, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
proj, voice, speed, out = pathlib.Path(sys.argv[1]), sys.argv[2], float(sys.argv[3]), pathlib.Path(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
home = pathlib.Path.home() / "models/kokoro"
k = Kokoro(str(home / "kokoro-v1.0.onnx"), str(home / "voices-v1.0.bin"))
lang = "en-gb" if voice[0] == "b" else "en-us"
script = json.loads((proj / "script.json").read_text())
for take in script["takes"]:
    parts, sr = [], 24000
    for ln in take["lines"]:
        a, sr = k.create(ln["spoken"], voice=voice, speed=speed, lang=lang)
        parts += [a.astype(np.float32), np.zeros(int(sr * 0.7), np.float32)]
    sf.write(out / f"{take['take']}.wav", np.concatenate(parts[:-1]), sr)
    print(take["take"], f"{sum(len(p) for p in parts[:-1]) / sr:.1f}s")

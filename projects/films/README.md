# Films (cinematic-film skill)

Narrated documentary-style films drawn in code. Engine and workflow: `plugins/motion-studio/skills/cinematic-film/` (read its `SKILL.md`, including the Adsworm notes at the end).

| Film | Length | What it is |
|---|---|---|
| `diwali-spike/` | 1:31, 1920x1080 | "The Diwali Spike": what 18 of our ad accounts showed, September to the three days after Diwali 2026. No client is named |

## Rebuild a film

```bash
S=plugins/motion-studio/skills/cinematic-film/scripts; PY=~/.venvs/cinematic/bin/python; P=projects/films/<slug>
$PY $S/get_fonts.py --project $P && $PY $S/prep_assets.py --project $P        # fonts and board textures
$PY $S/render.py --project $P --cues && $PY $S/build_sfx.py --project $P       # sound effects from the scene
$PY $S/mix_soundtrack.py --project $P --lufs -14                               # voice + effects
$PY $S/render.py --project $P --size 1920x1080 --out out/final.mp4 --audio audio/mix.m4a
$PY $S/burn_captions.py --project $P --video out/final.mp4 --audio audio/mix.m4a --style clean --out out/final_captions.mp4
```

`audio/narration.m4a` and `audio/timing.json` are kept in git, so the picture rebuilds without a voice step.

## A new voice

- **Higgsfield (house voice):** one take per section, saved as `audio/takes/<take>.wav`; then `split_takes.py` and `build_narration.py --tail <seconds>`.
- **Free, when credits are out:** `tools/kokoro_takes.py PROJECT VOICE SPEED OUT_DIR` writes the takes with Kokoro (open-source, Apache-2.0, runs on this machine). Setup: `pip install kokoro-onnx soundfile` into the cinematic environment, and the two model files from the kokoro-onnx GitHub release (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) in `~/models/kokoro/`.
- **Check any take before building:** `tools/heard_en.py PROJECT TAKES_DIR` prints what a speech recogniser hears, against the script.

# Reel 05 — "Meta changed 3 things" (English, clear explainer)

Reel 03's format (receipts card on top, two characters talking below, speech-bubble captions), rebuilt in plain English: Aman (face-matched 3D) explains, **Riya**, a brand owner (Indian English voice), asks what a client would ask. 50.4 s · 1080×1920 · −14 LUFS · spec PASS.

```bash
export REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
npm run voice                              # script/dialogue.mp3 → public/voice.wav + src/reel/timeline.json
node scripts/qa.mjs                        # stills per line → out/qa/sheet-*.png
node scripts/render-reel.mjs --no-voice    # → out/REEL-05_9x16.mp4 + out/cover.png
```

- **Voice:** the whole conversation is ONE ElevenLabs v4 dialogue call (Higgsfield `generate_audio`, model `elevenlabs_v4`, `dialogue` = the `say` lines with the voice ids in `script/script.json`). Saved as `script/dialogue.mp3`. If you change a `say` line, regenerate the dialogue. `voice.py` cuts pauses to 0.26 s and aligns Whisper word timings to the script.
- **Avatars:** `brands/adsworm/avatar-refs/aman-3d-sheet-v2.png`, `client-3d-sheet-v1.png` → `python3 scripts/avatars.py aman=…:idle,point,palms riya=…:idle,ask,wow`.
- **Facts:** `script/sources.md`.
- **Before posting:** wire comment keyword **META** → DM with the checklist PDF (links in sources.md). Turn on Instagram's AI label (AI characters + AI voices). The day count is calculated from today's date when `npm run voice` runs. If you post on a later day, run it again and re-render, because the voice track isn't regenerated.

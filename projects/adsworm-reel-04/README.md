# Reel 04 — "Meta quietly changed 3 things before Q4" (engine v2, English)

One flying camera over one canvas, THE ALGORITHM (coded orb) vs Aman (face-matched 3D avatar), word-synced captions, synthesized SFX. 39.5 s, 1080×1920, −14 LUFS, spec PASS.

```bash
export REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
npm run voice            # dialogue mp3 → tightened public/voice.wav + src/reel/timeline.json (Whisper word timings)
python3 scripts/sfx.py   # whooshes / punches / glitches from the timeline → public/sfx.wav
node scripts/qa.mjs 0 270 600   # stills → out/qa/sheet-*.png
node scripts/render-reel.mjs --no-voice   # → out/REEL-04_9x16.mp4 + out/cover.png
```

- **Voice:** whole dialogue in ONE ElevenLabs v4 call via Higgsfield (`script/script.json` voices: Aman = Holden, ALGO = Anika). Source mp3: `script/dialogue-v1.mp3`; `voice.py` caps silences at 0.2 s and speeds 1.06× (pitch kept) — the fix for choppy delivery.
- **Facts:** `script/sources.md`. UI mocks are tagged ILLUSTRATIVE UI. Post with Instagram's AI label.
- **Owner to-do before posting:** wire comment keyword **Q4** → DM (checklist PDF with the links in sources.md).

# Explainer reel engine v4 (one engine, many reels)

A teacher (Aman) and a student (Riya) as talking heads with lip-flap and facial reactions, karaoke bubble captions, a proof board that builds on the spoken word, sound played by the visuals, an open-loop chip held until the payoff. 1080×1920, 30 fps, −14 LUFS.

Rules and schema: `plugins/motion-studio/skills/explainer-module/` (SKILL.md, `references/retention-rules.md`, `references/script-schema.md`). Research behind them: `docs/playbook/`.

```bash
export REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
export REEL=late-replies                       # a folder in reels/

python3 scripts/draft_voice.py                 # free edge-tts draft → reels/$REEL/dialogue.draft.mp3
DIALOGUE=dialogue.draft.mp3 python3 scripts/voice.py   # → public/voice.wav + src/reel/timeline.json
python3 scripts/qa_report.py                   # pacing, holds, reactions, caption speed, payoff %, unspoken cues
node scripts/qa.mjs                            # a still per line → out/qa/sheet-*.png

python3 scripts/dialogue.py                    # prints the ONE ElevenLabs v4 dialogue request → save audio as reels/$REEL/dialogue.mp3
python3 scripts/voice.py && python3 scripts/qa_report.py
node scripts/render-reel.mjs --no-voice        # → out/ADSWORM_$REEL_9x16.mp4 + _cover.png   (FRAMES=0-240 for a quick check)
```

| Path | What |
|---|---|
| `reels/<slug>/script.json` | lines, captions, acting, board views, loop, payoff (one file drives everything) |
| `reels/<slug>/dialogue.mp3` | the whole conversation, one ElevenLabs v4 dialogue call (tags like `[laughs]` come from `tags`) |
| `reels/<slug>/sources.md` | every fact on screen with its source and date |
| `scripts/voice.py` | cuts quiet pauses, Whisper word timings aligned to the script, payoff breath, ducked pad |
| `scripts/sfx.py` | synthesizes `public/sfx/*.wav` (numpy only) |
| `scripts/faces.py` | aligns AI-edited expression frames to the base bust → `public/faces/` |
| `src/reel/Reel.tsx` | layout, acting, board motion, loop chip, payoff sound |
| `src/reel/views.tsx` | script items → components (`board.tsx`, `board2.tsx`, `receipts.tsx`) |
| `src/reel/Sfx.tsx` | a visual plays its own sound, pitch-varied |

Before posting: wire the comment keyword to a DM (ManyChat or Meta Business Suite), turn on Instagram's AI label (AI characters and voices), upload the `_cover.png`. Reels with a `{days}` countdown: rerun `voice.py` and the render on the posting day (no new voice needed).

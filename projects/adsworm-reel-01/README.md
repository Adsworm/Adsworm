# FULL CHAIRS 01: Adsworm reel, made 100% in code

A 34 s 9:16 reel for @adsworm, plus a 5-slide carousel, built with Remotion and the `motion-studio` skills. The music and SFX are synthesized in Python. There is no camera, no stock footage, no samples and no AI generation.

| File | What |
|---|---|
| `plan.md` | Account audit, content system and concept (reviewed by the creative-director agent) |
| `storyboard.md` | Second-by-second plan: frames, copy, motion and sound |
| `POSTING.md` | Caption, pinned comment, profile fixes, series queue |
| `src/reel/timeline.json` | Single source of truth for frames, music sections and SFX cues |
| `src/reel/` | Scenes and components: Words, AdCard, ClinicIcon, CommentField, LogoDraw |
| `src/carousel/` | "The 3 checks" carousel, built from the same components |
| `scripts/sound.py` | Code-synthesized score and SFX → `public/reel-audio.wav` |

```bash
npm install && pip install numpy scipy
npm run studio        # live preview
npm run qa            # 16 key-frame stills with safe zones → out/qa/sheet-*.png
npm run render        # sound → render → two-pass −14 LUFS master → out/FULL-CHAIRS-01_9x16.mp4 + out/cover.png
npm run carousel      # out/carousel/slide-1..5.png (1080×1350)
```

On a headless box, set `REMOTION_BROWSER_EXECUTABLE` to an existing Chromium headless shell.

**Next episode:** copy this folder, change the copy in the scenes, and update `timeline.json`. The audio follows automatically.

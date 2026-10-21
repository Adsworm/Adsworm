# THE BEST NEVER WINS: Adsworm reel 02, made 100% in code

This reel follows the adsworm.com brand: navy-black, cream, electric blue, gold, Bebas Neue and DM Sans. It is a consumer-psychology explainer: the mere-exposure effect, social proof and the halo effect. It lands on "WE DON'T RUN ADS. WE BUILD EMPIRES."

There is no camera, no stock, no samples and no AI generation. The score and SFX are synthesized in `scripts/sound.py` (drone, braam, taiko, swells, pulse).

| File | What |
|---|---|
| `storyboard.md` | Second-by-second plan (creative-director approved, all required changes applied) |
| `POSTING.md` | Caption, pre-post checklist, campaign plan, next 6 episodes |
| `src/reel/timeline.json` | Frames, music sections and SFX cues, shared by the picture and the sound |
| `src/reel/Stage.tsx` | The world: blue light beam, grid floor, bloom cues |
| `src/reel/Headline.tsx` | Bebas slam-in type with blue and gold accents and a light sweep |
| `src/reel/Skyline.tsx` | The "empire" night skyline |

```bash
npm install && pip install numpy scipy
npm run studio     # live preview
npm run qa         # 18 key-frame stills with safe zones → out/qa/sheet-*.png
npm run render     # sound → render → two-pass −14 LUFS master → out/THE-BEST-NEVER-WINS_9x16.mp4 + out/cover.png
```

# Reel 03 — the Hinglish explainer module (avatars + receipts + synced voice)

A code-rendered version of the Instagram module that is working for Indian Meta-ads educators: two flat-vector characters have a Hinglish conversation under a "receipts" card, with one short caption per line and blue keyword pills. Picture, captions and card builds are all driven by the neural-TTS word timings, so they can't drift.

| Piece | File |
|---|---|
| Script (voice text in Devanagari-mixed Hinglish, captions in Latin Hinglish with `[pills]`, beats, poses, `paid` overrides, live countdown) | `script/script.json` |
| Sources for every fact on screen | `script/sources.md` |
| Dissection of the reference reel | `script/reference-analysis.md` |
| Voice + mix + timeline engine (edge-tts neural voices, cached by text+voice+rate) | `scripts/voice.py` |
| Avatar sheet → per-pose transparent PNGs | `scripts/avatars.py` |
| Card content per section | `src/reel/beats.tsx` |
| Receipt primitives (browser, phone, chat, bars, chart, comment UI, PDF…) | `src/reel/receipts.tsx` |
| Posting kit | `POSTING.md` |

```bash
npm install && pip install edge-tts numpy scipy pillow
npm run voice                       # script.json → public/voice.wav + src/reel/timeline.json (only changed lines are re-synthesised)
npm run qa                          # one still per spoken line, safe zones on → out/qa/sheet-*.png
npm run render                      # voice → render → −14 LUFS master → out/REEL-03_9x16.mp4 (+ cover.png)
REEL_NAME=MY-NAME npm run render -- --no-voice   # reuse the existing voice/timeline
npm run render -- --paid            # boosted-post variant: "DM DIWALI" end card + its spoken line → out/REEL-03_PAID_9x16.mp4
REEL_DAYS=16 npm run render         # force the countdown number (default: days from today to vars.countdown.to)
```

Avatars were generated once (Nano Banana Pro via Higgsfield, 2 credits each) and keyed/split with `scripts/avatars.py`. Replace `public/avatars/*.png` with a likeness of the founder when a reference photo is available.

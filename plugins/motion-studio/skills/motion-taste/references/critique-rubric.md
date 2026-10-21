# Motion critique rubric

Score each line from 1 to 5 using the contact sheet (`npm run qa`) and, once it exists, the full render. **Ship at ≥ 4.0 average with no line below 3.** Fix the three lowest scores first. Never fix more than three things per pass, and cap QA at three passes. Log every pass in `review.md`.

| # | Criterion | 5 looks like | Common fail |
|---|---|---|---|
| 1 | Thumb-stop (frame 0–15) | Hook or product is legible on frame 0 and motion starts by f15 | Empty background fading in |
| 2 | Message clarity, sound off | A stranger can say the offer after one muted view | The story lives only in the VO |
| 3 | Phone legibility | Readable at 375 px wide; body ≥ 36 px at 1080 | 28 px labels, thin weights on busy backgrounds |
| 4 | Safe zones | Nothing critical in the red overlay | CTA under the Reels caption area |
| 5 | Hierarchy | One focal point per beat | Three things move at once with equal weight |
| 6 | Easing quality | outExpo entrances, springs only on physical objects, no linear UI | Linear slides, bounce everywhere |
| 7 | Timing and holds | ~3 words/s + 0.5 s, holds have ambient idle | Rushed offer, dead freeze frames |
| 8 | Rhythm | Arrivals land on beats; transitions consistent | Random timing, mixed transition styles |
| 9 | Brand fidelity | Exact colors and fonts, logo per guidelines, voice matches | Default fonts, off-hex colors |
| 10 | Polish | Grain or texture, no pops or flicker, no text collisions or overflow | Single-frame pops, clipped descenders |
| 11 | Claims and compliance | Every claim approved and legal lines present | Invented stats |
| 12 | CTA | Holds ≥ 2 s, high contrast, one action | Two CTAs, or the CTA fades out early |

## How to look at a contact sheet

1. Read the PNG and go left to right: hook → product → stats → offer → final frame.
2. For each still, ask what the eye hits first, whether the type is legible at thumbnail size, and whether anything touches the red zones.
3. Compare formats side by side (9:16 vs 4:5 vs 1:1). Proportions should feel identical, not cramped in square.
4. For motion problems a still can't show (pops, stutter), render a 2–3 s range: `npx remotion render src/index.ts Ad-9x16 out/clip.mp4 --frames=60-150 --scale=0.5`.

## review.md entry format

```
Pass 2 — avg 3.8 — lowest: #3 legibility (2), #7 timing (3), #4 safe zones (3)
Fixes: stat labels 28→38px; offer hold 40→70f; CTA moved above 35% bottom zone
```

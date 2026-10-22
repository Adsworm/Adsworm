---
name: explainer-module
description: The voice-led Instagram explainer format that holds retention — two cartoon avatars in a Hinglish dialogue under a "receipts" card, captions and card builds synced to neural-TTS word timings, numbered news breakdown, comment-keyword CTA. Use for educational/news reels for a business audience; use instead of kinetic-typography when the goal is watch time and comments.
---

# Explainer Module

Kinetic typography over a dark background gets skipped: no voice to follow, nothing concrete to believe, and Instagram deprioritises "majority text" reels. This module is what works for Indian business/marketing educators in 2026. Template project: `projects/adsworm-reel-03` (copy it; edit `script/script.json`; run `npm run render`).

## Retention architecture (non-negotiable)

| When | Beat | Rule |
|---|---|---|
| 0–2 s | Hook line spoken from frame 0; card already shows the hook number (frame 0 is the thumbnail) | Identity call-out + specific number + novelty: "Founder ji, Diwali mein 17 din, aur Meta ne 3 cheezein badal di" |
| 2–5 s | Second voice objects ("Abhi? Mera budget set hai") → promise ("teeno paisa bachaate hain") | Dialogue, not monologue; the objection is what the viewer is thinking |
| 5–60 s | Countdown ①②③, each: mini-hook → receipt builds while the voice says it → founder reaction | A receipt (official page, UI mock, chart) lands every 3–5 s; biggest item last |
| then | Bonus insight with a chart; CTA "Comment X" with a comment-UI mock + PDF tile; "Save, send to partner" | Comments and sends are ranking signals |

- **Line length ≤ 9 words**; one line per caption; 1–2 `[pills]` per line; ~2.5 s per line; keep it 45–75 s.
- **Facts only with receipts** on the card (URL bar + title + date, source line at the bottom). Write them to `script/sources.md` first.
- **Light theme** (paper, white cards, one brand blue, gold for numbers). Dark cinematic reads as an ad.
- **Audio:** the voice is the timing track. A beatless pad 20+ dB under the voice, UI pops that land with the elements. No beat-driven music, no SFX leading the visual.

## Pipeline

1. `script/script.json`: per line `who`, `say` (Devanagari for Hindi words so TTS pronounces them right), `show` (Latin-script Hinglish with `[pills]`), optional `beat` and `pose`. Rates: AMAN `+40%`, FOUNDER `+46%` (hi-IN neural voices speak ~2 w/s at default; the reference pace is ~3 w/s). Avoid `!`, `…`, `।` in `say` — each adds a 0.5–0.9 s pause.
2. `npm run voice`: edge-tts per line (word boundaries) → `public/voice.wav` + `src/reel/timeline.json` (lines, sections, beats = frame each beat starts).
3. `src/reel/beats.tsx`: card content per section built from `receipts.tsx` primitives, each revealing from its beat frame.
4. `npm run qa`: a still 8 frames into every line. Read every sheet. Check: frame 0 complete, no empty card at any section start, chips not wrapping, captions ≤ 2 lines, nothing in the bottom 35%.
5. `npm run render`: two-pass −14 LUFS master. Run `meta-delivery-qa` on the MP4.

## Avatars

Generate one character sheet per person (3 poses side by side, flat 2D vector style, solid green background) — Nano Banana Pro via Higgsfield costs ~2 credits — then `python3 scripts/avatars.py who=sheet.png:pose1,pose2,pose3`. The speaker gets point/thumbs/idle poses, the listener idle/think/wow. For a founder likeness, pass a reference photo to the image model.

## Upgrades
- ElevenLabs voices (`elevenlabs/skills` text-to-speech) replace edge-tts for a more natural Hinglish delivery: same `say` text, same word timings.
- For the paid (boosted) version, change the CTA to "DM <keyword>" (one prop) — comment CTAs are for organic.

# 05 · Captions, titles and brand

Rendered in Remotion (`remotion/`) to a transparent ProRes 4444 overlay (`--color-space=bt709`), then composited by `scripts/finish.sh`. Both systems take props built from source-timed phrase files, so a cut change never desyncs captions.

## System A: editorial (`Overlay` composition)
- Accent words set in Gloock (serif) in the brand accent colour; the rest in Instrument Sans SemiBold, ivory.
- Words arrive one by one (eased rise and fade). `hero` pages set the accent word large.
- Builder: `scripts/build_captions.py edl.json phrases.json words.json outdir name --endcard 2.6`
- Phrase format: `{"s":src_start,"e":src_end,"text":"line one|line two","hl":["word"],"hero":false}`

## System B: two-tier (`TeamOverlay` composition), matched from an agency edit
- Measured by shape matching (`scripts/font_match.py`, IoU 0.79 against the next best at 0.64): **Inter Tight**.
  - White line: ~54 px Medium, #F0ECE2.
  - Gold line: ~76 px SemiBold, #C7AF83.
  - Centred at 69% of frame height, words blur in.
- Optional serif title pill ("Client Testimonial") at the start: Gloock, frosted, with a thin outline.
- Logo line ("The place is" plus the client's vector logo).
- Builder: `scripts/build_captions_team.py edl.json phrases_team.json props.json out.srt --endcard 2.6`
- Phrase format: `{"s":…,"e":…,"lines":["white line","*gold line"],"logo":false}` (a `*` prefix makes a line gold).

## Rules
- 1–2 lines, max ~820 px wide at 1080, never over the face, inside Instagram's safe area (avoid the bottom 18% and the right-hand button column).
- Check accent colours over the brightest object in shot (a white table). Champagne or gold on white needs a soft dark radial glow behind the text. Do not use a box, and do not use a full-frame scrim (it lifts blacks and reads as haze).
- Proper-noun spelling comes from the client, not from ASR.
- Fonts must be licensed (SIL OFL fonts are in `remotion/public/fonts` with their licence files). If a team uses a commercial font (e.g. SF Pro, which is Apple-only), match it with an open one and say so.

## Identifying a team's font from a video
1. Extract frames where the text sits on its darkest background, then build a mask by colour (gold: R>150, R−B>45; white: all channels >215).
2. Render the same words in candidate fonts across weights, scale to the reference height, and score IoU with shift search (`font_match.py`).
3. When masks are unreliable (light text on light pill), compare a rendered candidate strip visually.

## Logo
Never retype a logo. Extract the client's vector paths from their PDF (`logo_to_svg.py` converts the extracted JSON) and recolour only.

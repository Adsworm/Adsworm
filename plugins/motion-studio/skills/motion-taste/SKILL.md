---
name: motion-taste
description: Premium motion rules and a scored critique rubric — easing, timing, hierarchy, type, sound, anti-slop bans. Use while animating and when reviewing frames.
---

# Motion Taste

Generic AI motion has a look: everything bounces, glows, crossfades and sits dead-center. Premium motion is restraint plus intent. Apply these rules while you build, then score the result with `references/critique-rubric.md`.

## Easing and timing

| Use | Curve / config | Duration @30fps |
|---|---|---|
| Entrances (type, UI, product) | outExpo `cubic-bezier(0.16,1,0.3,1)` | 18–24 f |
| Scene transitions | inOutQuart `cubic-bezier(0.76,0,0.24,1)` | 12–16 f |
| Exits (rare: cut instead) | inExpo `cubic-bezier(0.7,0,0.84,0)` | 8–12 f |
| Physical objects (product, cards) | spring mass 1, stiffness 180, damping 20–22 | settles ≈ 20 f |
| No-overshoot glide | Remotion `{damping: 200}` | — |
| CTA pop | spring damping 12, stiffness 180, mass 0.6 | one pop only |

- **Never use linear easing** on UI or type. Reserve it for tickers, progress bars and constant drift.
- **Stagger** 3–6 f per word or item, and 8–10 f per card. Every element arriving together reads as a slide deck.
- **Hold:** about 3 words per second plus 0.5 s. A hold is never motionless. Keep an ambient idle going (float of about 1% of height, slow glow drift, grain).
- **Rhythm:** on music, land key moments on beats. Build the beat map before animating.

## Hierarchy and layout

- Give each beat **one focal point**. The eye should know where to go within 200 ms.
- Use a type scale keyed to the short edge, with display at about 12% of the short edge. Mobile is the canvas: body text at 1080 px wide should be ≥ 36 px.
- Respect the safe zones. In 9:16 Reels, keep text and logos out of the top 14%, bottom 35% and 6% sides.
- Vertical is a **re-layout**, not a crop. Stack the content and resize it, don't just scale it.

## Typography

- Use **two families at most**: a tight grotesk for display (tracking about −0.04em) plus one accent face, such as a serif italic for the emotional word.
- Accent one to three words per line at most. Accenting everything means nothing is accented.
- Animate words, not letters, for anything longer than 3 words. Mask reveals (rise from the line box) read premium. Typewriters read cheap unless the concept is literally typing.

## Color and texture

- Use the 60/30/10 split: paper/ground, ink/primary, accent. The accent marks the money moment (offer, CTA).
- Text contrast must be ≥ 4.5:1 (WCAG AA). Over footage, always use a scrim.
- Add subtle film grain (opacity about 0.05–0.08) and soft drifting light. Flat vector fills look rendered.

## Banned unless the brief asks for them

Random particles, lens flares, generic neon glows, bounce on every element, 3D card flips, crossfade on every cut, rotating 3D text, spinning logos, stock whoosh on every move, center-everything for the whole video, gradient-mesh blobs as the only idea, emoji confetti.

## Sound (Meta autoplays muted)

- The piece must work **sound-off**: the story reads from type alone.
- **Sound-on:** use one soft SFX per meaningful arrival and silence otherwise. Music ducks under VO. Master to −14 LUFS integrated, with true peak ≤ −1 dBTP.

## Ad-specific rules

- **Frame 0** is the thumbnail and the thumb-stop. It must show the hook or the product, never an empty background fading in.
- The brand appears in the first 3 s, at least as a small wordmark.
- The offer and CTA hold ≥ 2 s and sit inside the safe zone.
- Every claim on screen is in the approved-claims list.

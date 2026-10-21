---
name: brand-motion-system
description: One brand file per client (colors, fonts, logo, voice, claims, motion personality) compiled into Remotion/HyperFrames/GSAP settings. Use when onboarding or switching clients.
---

# Brand Motion System

An agency's failure mode is drift: last client's gold accent showing up in this client's ad. Each client gets exactly one folder, and every engine reads from it.

## Folder layout

```
brands/<client>/
  brand.json        source of truth (schema below)
  logo.svg          primary lockup (+ logo-mono.svg, logo-mark.svg)
  fonts/            licensed files only (license file next to them)
  product/          transparent cut-outs, 2000px+ tall
  claims.md         approved claims with source + approval date — nothing else goes on screen
```

**Session rule:** confirm which client before touching anything, load only that brand folder, and never copy assets across client folders.

## brand.json

```json
{
  "client": "atelier-nine",
  "brandName": "ATELIER NINE",
  "colors": {"primary": "#1F3D2B", "accent": "#C9963F", "ink": "#151515", "paper": "#F3EEE6"},
  "fonts": {
    "display": {"family": "Inter Tight", "file": "fonts/InterTight-Variable.woff2", "license": "OFL"},
    "accent":  {"family": "Instrument Serif", "file": "fonts/InstrumentSerif-Italic.woff2", "license": "OFL", "style": "italic"}
  },
  "logo": {"primary": "logo.svg", "minWidthPx": 160, "clearSpace": "1x cap height", "never": ["recolor", "outline", "rotate"]},
  "voice": {"is": ["calm", "clinical", "warm"], "isNot": ["hype", "slang", "ALL CAPS shouting"]},
  "motion": {"personality": "luxury"},
  "banned": ["particles", "neon glow", "bounce"],
  "legal": ["Results vary. Based on a 4-week consumer study, n=112."]
}
```

## Motion personalities → settings

| Personality | Entrances | Easing / spring | Transitions | Stagger | Feel |
|---|---|---|---|---|---|
| `luxury` | 24–36 f | outExpo; spring `{damping: 200}` | fade, slow wipe | 6–8 f | one element per beat, negative space, serif accents |
| `performance` | 12–18 f | spring `{damping: 20, stiffness: 200}` | push-cut, slide | 3–4 f | punchy, stacked benefits, price anchors |
| `tech` | 16–22 f | inOutQuart | slide, wipe | 4–5 f | grid, UI recreated in code, monospace details |
| `playful` | 14–20 f | spring `{damping: 12}` (pop) | slide, zoom | 4 f | color blocks, bigger type, still no particles |

## Compile to each engine

- **Remotion kit:**
  1. Write `props/<client>.json` with `brandName` and `colors`.
  2. Copy the fonts into `public/fonts` and update `src/lib/fonts.ts` (family names must match).
  3. Copy the logo into `public/` and set `logo`.
  4. Map the personality onto the durations and springs in `lib/motion.ts` and the timeline frame counts.
- **HyperFrames:** put the palette, type, personality table row, voice and bans into the project's design/brief file, so `/hyperframes-creative` reads it on every scene.
- **GSAP:** register eases with `CustomEase.create("brandOut", "0.16,1,0.3,1")` and `CustomEase.create("brandInOut", "0.76,0,0.24,1")`.
- **CSS / HTML statics:** `--brand-primary`, `--brand-accent`, `--brand-ink`, `--brand-paper`, `--ease-out: cubic-bezier(0.16,1,0.3,1)`.
- **Gen-AI prompts** (Higgsfield/fal/Runway): append the palette as words ("deep forest green, warm gold, cream"), the voice and "no text in frame". Type is always added in code.

## Onboarding checklist

1. Collect the logo as vector, brand colors (verify the hex codes against the live site), font files and licenses, 3 reference ads they love and 3 they hate, approved claims, and legal lines.
2. Fill in `brand.json` and `claims.md`, and pick a personality.
3. Render one QA sheet with the client's props. Get sign-off on that look before any campaign work.

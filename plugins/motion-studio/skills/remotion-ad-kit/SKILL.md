---
name: remotion-ad-kit
description: Premium Remotion ad template — one prop set renders 9:16/4:5/1:1/16:9 video plus static PNGs, with QA contact sheets and variant batches. Use to build or extend coded ads.
---

# Remotion Ad Kit

This is a production template, not a demo. It was verified rendering a 12.6 s 1080×1920 ad in about 45 s on a 4-core container.

## Scaffold

```bash
rsync -a --exclude node_modules --exclude out "${CLAUDE_SKILL_DIR}/template/" ./<project>/
cd <project> && npm install
npm run studio        # live preview at localhost:3000 (props are editable in the right panel)
```

On a headless box with no Remotion browser download, point at an existing Chromium: `export REMOTION_BROWSER_EXECUTABLE=/path/to/chrome-headless-shell`.

## Commands

| Command | Output |
|---|---|
| `npm run qa -- [props.json] [Ad-9x16 …]` | `out/qa/<id>-sheet.png`: 5 stills with safe-zone overlay. **Read the sheet** before any full render |
| `npm run render:all -- [props.json] [Ad-9x16 …]` | `out/Ad-<fmt>.mp4`, encoded H.264 High, yuv420p, BT.709, CRF 18 |
| `npm run stills -- [props.json]` | `out/static/Static-<fmt>.png`: static ads from the same props |
| `npm run variants -- <matrix.json> [--dry-run]` | `out/variants/*.mp4` + `manifest.csv` (see `ad-variant-matrix`) |
| `npm run typecheck` | tsc |

A props JSON is shallow-merged over `defaultAdProps`, so pass the whole `colors` object if you change any color.

## Props (`src/schema.ts`)

| Prop | Notes |
|---|---|
| `brandName`, `colors.{primary,accent,ink,paper}` | From the client brand file |
| `hook`, `headline`, `offer` | Wrap words in `*asterisks*` to get the serif-italic accent |
| `subline`, `cta` | Plain text |
| `stats[]` | 0–3 items: `{value, prefix, suffix, label}`. An empty list drops the stats scene, and the duration recalculates |
| `productImage`, `logo`, `music`, `backgroundVideo` | File names in `public/`. Empty = off. `backgroundVideo` is the hybrid lane: AI or shot footage under the coded type, with a legibility scrim |
| `showSafeZones` | Dev overlay. QA forces it on |

The template's defaults are a placeholder brand (ATELIER NINE) with **placeholder claims**. Replace every stat with substantiated numbers.

## Architecture

```
src/schema.ts       props + defaults (zod → editable in Studio)
src/Ad.tsx          buildTimeline() = scene order/length, single source for duration
src/StaticAd.tsx    static layout; PNG = last frame of a 111-frame comp
src/scenes/         HookScene, ProductScene, StatsScene, EndCard
src/components/     KineticText, ProductShot, StatCounter, CTAButton, Wordmark,
                    Background (drifting glows), Grain (film grain), SafeZoneOverlay, FadeUp
src/lib/motion.ts   easing curves, spring presets, progress(), alpha()
src/lib/layout.ts   format detection, Meta safe zones, type scale keyed to short edge
src/lib/fonts.ts    local fonts in public/fonts (OFL), so renders never hit the network
```

## Extending

- **New scene:** create `src/scenes/X.tsx`, which reads `useLayout()` for padding and type, then add `{id, frames, node, enter}` to `buildTimeline`. Transitions are 14 frames. Duration updates itself.
- **Client fonts:** drop the files in `public/fonts` and edit `lib/fonts.ts`. Keep one grotesk and one accent face, and record the font license in the brand file.
- **Layout rule:** never hard-code pixels. Use `type.*`, `pad.*` and `unit` from `useLayout()` so every placement stays in proportion.
- **Motion rule:** use `ease.*` and `springs.*` from `lib/motion.ts`. Never use linear easing on UI elements, and never use `Math.random()`/`Date.now()`. Follow `motion-taste`.
- **Remotion-specific depth** (captions, 3D, audio viz, maps, Lottie): see the official Remotion skills.

## Gotchas found while building this kit

- **Remote Google Fonts:** they can fail to load in sandboxed or proxied Chromium, and the render aborts. Fonts are therefore bundled locally.
- **`<Freeze>` in Remotion 4.0.537:** it did not settle animations in still renders. Statics instead render the last frame of a short composition.
- **Remotion's default pixel format:** it can tag output full-range (`yuvj420p`). The scripts force `yuv420p` and BT.709 so colors don't shift after Meta re-encodes.
- **Stat rows:** they size numbers to their column and wrap labels, so long values like "14 days" don't break onto two lines.

## License (read before agency use)

Remotion is free only for individuals and companies of **≤3 people**. Headcount counts everyone, not just users. Above that you need a Company License (https://remotion.pro): Creators at $25/seat/month, or Automators at $0.01/render with a $100/month minimum. The `render:all` and `variants` scripts call `renderMedia()` programmatically, which Remotion classes as automation. Set `REMOTION_LICENSE_KEY` once you are licensed. If licensing is a blocker, route the job to HyperFrames (Apache-2.0).

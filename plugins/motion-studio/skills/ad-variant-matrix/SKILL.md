---
name: ad-variant-matrix
description: Hooks × offers × CTAs × placements → batch render with Meta-ready names and a manifest. Use for ad variations, creative testing, or "make 20 versions".
---

# Ad Variant Matrix

Variant velocity is the premium moat. 24 on-brand, QA'd and correctly named variants beat one hero film for Meta's learning phase.

## 1. Design the test before rendering

- **Change one dimension per test round** if you want to learn something: hooks first (they move hook rate the most), then offers, then CTAs. Crossing all axes at once is for volume, not learning.
- **Keep the count sane:** 3 hooks × 2 offers × 1 CTA × 2 formats = 12 renders. Every render costs CPU time and, if you're licensed, Remotion Automator fees.
- **Hooks must differ in angle, not wording:** pain, outcome, curiosity, social proof, contrarian. Five synonyms of the same hook teach nothing.

## 2. Write `props/matrix.json`

```json
{
  "campaign": "ATL9-VITC-LAUNCH",
  "base": "props/<client>.json",
  "formats": ["Ad-9x16", "Ad-4x5"],
  "axes": {
    "hook":  [{"id": "H1", "value": "Your skin *isn’t* tired. It’s *underfed.*"},
              {"id": "H2", "value": "Dull by 3pm? *Fix the cause.*"}],
    "offer": [{"id": "O1", "value": "Launch week — *20% off*"}],
    "cta":   [{"id": "C1", "value": "Shop the Serum"}]
  }
}
```

Any prop in the kit schema can be an axis: `headline`, `stats`, `colors`, `productImage`, `backgroundVideo` and so on. Axis IDs become part of the file name, so keep them short and stable across rounds (H1 stays H1 forever).

## 3. Dry-run, QA one, then render all

```bash
npm run variants -- props/matrix.json --dry-run   # prints names + render count, renders nothing
npm run qa -- props/<client>.json               # QA the base once; variants share its layout
npm run variants -- props/matrix.json              # out/variants/*.mp4 + manifest.csv
```

Spot-check the longest hook in each format with a QA sheet. Long copy is what breaks layouts. Then run every file through `meta-delivery-qa`.

## 4. Hand off

`manifest.csv` has one row per file: name, format, axis values, path and duration. Use the `name` column verbatim as the Meta ad name. Upload through Ads Manager bulk import or the Meta MCP (`ads_creative_upload_media` → `ads_create_creative` → `ads_create_ad`), **only with explicit user approval, and paused by default**.

## Scale beyond one machine

The local renderer handles dozens of files. For hundreds, deploy Remotion Lambda (`npx remotion lambda functions deploy`; about $0.02 per minute of video in compute) or switch to HyperFrames batch (JSONL on Lambda, no per-render license).

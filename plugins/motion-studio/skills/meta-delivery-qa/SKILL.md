---
name: meta-delivery-qa
description: Final gate for Meta ad files — script-checked specs per placement, safe zones, loudness, naming, handoff package. Use when exporting or delivering ads.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/check_specs.sh *)
---

# Meta Delivery QA

Nothing ships until every file passes the script and the human checks below.

## 1. Spec check (deterministic)

```bash
"${CLAUDE_SKILL_DIR}/scripts/check_specs.sh" out/Ad-9x16.mp4 reels
"${CLAUDE_SKILL_DIR}/scripts/check_specs.sh" out/Ad-4x5.mp4 feed
for f in out/variants/*.mp4; do "${CLAUDE_SKILL_DIR}/scripts/check_specs.sh" "$f" || exit 1; done
```

The placement argument is one of `reels`, `stories`, `feed`, `square`, `landscape` or `auto` (inferred from the aspect ratio).

- **FAIL** means the file must not ship. Causes: wrong aspect for the placement, file over 4 GB, fps over 60, or a bad container.
- **WARN** means house best practice, so fix it unless there's a reason. Examples: non-yuv420p pixel format, no audio, loudness outside −16…−12 LUFS, 9:16 longer than 15 s.

Specs change. Confirm current limits in Meta's Ads Guide (https://www.facebook.com/business/ads-guide) before a new placement or objective. See `references/meta-specs.md`.

## 2. Fixes for common failures

```bash
# Loudness → −14 LUFS, true peak −1 dBTP (two-pass is more accurate; one-pass shown)
ffmpeg -i in.mp4 -c:v copy -af loudnorm=I=-14:TP=-1:LRA=11 -c:a aac -b:a 192k out.mp4
# Full-range / odd pixel format → yuv420p BT.709
ffmpeg -i in.mp4 -vf "scale=in_range=full:out_range=tv,format=yuv420p" -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:v libx264 -crf 18 -preset slow -c:a copy out.mp4
# Too heavy for upload → constrain bitrate
ffmpeg -i in.mp4 -c:v libx264 -crf 20 -maxrate 12M -bufsize 24M -movflags +faststart -c:a copy out.mp4
```

## 3. Human checks (the script can't see these)

- **Safe zones.** Read the QA sheet (`npm run qa` overlays them). In 9:16, keep text and logos out of the top 14%, bottom 35% and 6% sides. Stories need about 14% top and bottom.
- **Frame 0 is the thumbnail.** It must carry the hook or the product.
- **Copy.** Spell-check the claims against the approved list, check legal lines are present, and check prices match the live offer.
- **Watch once muted on a phone.** Is the message clear?

## 4. Naming (wires into reporting)

`<CAMPAIGN>_<HOOK>-<OFFER>-<CTA>_<FORMAT>_v<N>.mp4`, for example `ATL9-VITC-LAUNCH_H2-O1-C1_9x16_v1.mp4`. Use the same string as the Meta **ad name**, so `creative-performance-loop` can map results back to creative attributes. `ad-variant-matrix` generates these names for you.

## 5. Handoff package

```
delivery/<CAMPAIGN>/
  social/      H.264 MP4s per placement (passed check_specs)
  statics/     PNG statics (npm run stills)
  masters/     ProRes 4444 with alpha for overlays/lower-thirds (--codec=prores --prores-profile=4444)
  captions/    .srt per video (burned-in version in social/ if the brief asks)
  manifest.csv (from ad-variant-matrix, or hand-written: name, placement, hook, offer, cta, duration)
  RIGHTS.md    fonts, music, stock, footage, AI-model terms — source + license + expiry per asset
```

Treat RIGHTS.md as part of the deliverable. Unlicensed music or fonts are the most common takedown cause.

# Meta placement cheat sheet

This reflects house defaults as of Oct 2026. Meta's own Ads Guide is the source of truth: https://www.facebook.com/business/ads-guide. When the two disagree, Meta wins. Update this file when that happens.

| Placement | Aspect | Render at | Safe zone (keep text/logos out) | House length |
|---|---|---|---|---|
| Reels (FB/IG) | 9:16 | 1080×1920 | top 14%, bottom 35%, sides 6% | 6–15 s |
| Stories (FB/IG) | 9:16 | 1080×1920 | top 14%, bottom 14% | 6–15 s |
| Feed (FB/IG) | 4:5 | 1080×1350 | ~6% margin all round | 10–30 s |
| Square / carousel | 1:1 | 1080×1080 | ~6% margin | 10–30 s |
| In-stream / landscape | 16:9 | 1920×1080 | ~7% vertical margin | per brief |

## Encoding house defaults

- **Video:** H.264 High, yuv420p, BT.709, CRF 18 (the kit's render scripts do this). 30 fps for motion graphics. Keep the source fps for footage.
- **Audio:** AAC 48 kHz, 192 kbps, −14 LUFS integrated, ≤ −1 dBTP.
- **Container:** MP4 with `+faststart`. Meta's video-ad file limit is 4 GB, but a 15 s ad should be well under 50 MB.

## Creative rules that matter more than specs

- **Plan for muted autoplay:** use burned-in captions or type-led storytelling.
- **Make native vertical cuts.** Don't letterbox 16:9 inside 9:16.
- **One message per ad.** Test messages across ads, not inside one.
- **Keep text density reasonable on statics.** Meta no longer hard-rejects at 20% text, but dense text still tends to cost delivery.

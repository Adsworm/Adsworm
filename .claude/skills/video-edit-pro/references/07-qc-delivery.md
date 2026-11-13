# 07 · QC and delivery

## Self-review before showing anything (measure, don't assume)
| Check | How | Pass |
|---|---|---|
| Duration and frames | ffprobe on the output | Equals the EDL; picture and audio the same length |
| Cut-off words | `probe_words.py` on isolated windows around every join and the last 2 s of speech, plus one whole-file pass with `asr_batch.py` | Every sentence complete; no new words |
| Caption sync | Caption start vs 1–4 kHz speech onset | Within ±0.10 s |
| Captions | One frame from every page, composited and viewed | Correct text, readable over the brightest object, clear of the face and the UI safe area |
| Loudness | `ebur128=peak=true` | −14 LUFS ±0.5, true peak ≤ −1 dBFS |
| Music level | Aligned-stem subtraction (see 06) | ≈ −20 dB under the voice in speech; audible under the end card |
| Skin consistency | Forehead-patch R/G and B/G in every segment | B/G spread < 0.02 |
| Stability | Background phase correlation, frame to frame | < 1 px at 1080 except real camera bumps |
| Crop | `render_base.py` clamp counter | 0 clamped frames |
| AI plates | Flicker ratio (see 03) | Change ratio ≤ detail ratio |
| End card | Pixel sample | Brand colours within 3 levels |
| Metadata | ffprobe format tags | No GPS, device or date |

The first job's QC caught a wrong final out-point, a music bed buried 33 dB down, a 9 px crop overshoot and gold text unreadable over a white table. Every one of these was invisible in the plan.

## Deliverables
- Social: `…_SOCIAL_1080x1920.mp4` (H.264 High 4.2, CRF 17, maxrate 16M, AAC 256k, faststart, Rec.709 tags, no metadata). Add a textless version if the platform's own captions might be used.
- Master: ProRes 422 HQ (composite once), then 10-bit HEVC (`hvc1`) derived from it. Files over 500 MB cannot be sent as attachments: offer a Drive upload, but only with explicit approval (it is client footage).
- SRT on the edit timeline, the voice stem, music alternates and the licence record.
- A project archive: EDL, phrase files, props, tracking and motion data, Remotion source and scripts.
- Variants: when the user asks for a version in a team's style, only the overlay changes. Picture, sound and timing stay identical so the variants are a fair comparison.

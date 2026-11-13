# 03 · Picture: stabilise, reframe, grade, dehaze, AI detail

All of this lives in `scripts/render_base.py` and is driven by `edl.json` → `grade`. Render **stills first** (`render_base.py still …`), compare them with the source and measure, then render video.

## Stabilise and reframe
- `face_track.py`: normalised cross-correlation on a head template, smoothed. It held all 905 frames on the first job (minimum match 0.58).
- `render_base.py prep`: camera drift by phase correlation on the background band. The crop is locked to the background, so handheld sway disappears while the speaker's own movement stays.
- Zoom: per-segment keyframes `[[source_frame, scale], …]`, interpolated with smootherstep and geometrically (an even perceived push). Before rendering, check that no frame's crop leaves the source; the bounds check is in the lessons file. Change shot size by at least 15% across a non-contiguous join (same-size joins read as jump cuts).
- Resolution: a 4K portrait source supports up to about 1.55 for a 1080-wide export without upscaling. Beyond that the face goes soft.

## Grade order (per frame, float, Rec.709 limited → full range on decode)
`dehaze → white balance → tone curve (LUT) → saturation → glare desaturation → face light / surround dim / vignette (tracked, feathered, built at 1/8 res) → split tone → multi-band luma detail (+ extra on the face) → clarity → grain`

Values that worked on a high-key clinic interior (cream wall, warm LED cove behind the subject):
```json
{"dehaze":0.30,"airlight":[1.0,0.97,0.92],"wb_gain":[1.03,0.995,0.965],
 "curve":[[0,0],[0.035,0.0],[0.12,0.08],[0.30,0.265],[0.50,0.495],[0.70,0.715],[0.86,0.86],[1.0,0.955]],
 "saturation":1.08,"glare_desat":0.35,"shadow_tint":[-0.008,0.003,0.005],"highlight_tint":[0.004,0.002,-0.006],
 "face_lift":0.05,"background_dim":0.16,"vignette":0.12,"detail":[[0.7,0.7],[2.2,0.35]],"face_detail":0.35,
 "clarity":0.10,"glow":0,"grain":0.003}
```

## "Hazy / glare / face not clear": diagnose before you fix
Render the same frame at each grade stage and measure face p2/p50/p98, black level around the hair, mid-band detail energy and wall luma. On the first job the haze had four causes:
1. **Source backlight veiling glare**: the LED cove directly behind the head lifted the darks (face black level 18/255 before any grade). Fix: dark-channel dehaze with a guided-filter veil (no halos at hair edges), strength 0.3; highlight roll-off to 0.955; glare desaturation.
2. **Phone noise reduction** had erased fine detail. Fix: multi-band luma sharpening (radii 0.7 and 2.2 px) with extra weight inside the tracked face mask, plus optional AI detail (below).
3. **Our face lift (+14%)** pushed the face toward the bright wall and flattened it. Fix: face +5% and surround −16%. Separate by darkening the surround, not by brightening the face.
4. **Our full-width scrim and bloom**: a dark gradient behind the captions lifted black from 1 to 5 (milky), and "glow" added bloom around a backlit head. Fix: no bloom on backlit subjects; replace the scrim with a soft per-caption glow.

## AI detail (optional, only when the client asks for "clearer faces")
- Model: Real-ESRGAN general x4v3 (`SRVGGNetCompact`, BSD-3, safetensors from Hugging Face) loaded via spandrel on CPU.
- `scripts/sr_plates.py <src> track.json <model> <out> half <ranges>`: crop 480×600 around the tracked face, downscale ×0.5, run ×4, return to the crop size. About 1.3 s/frame on 4 cores.
- **Detail-max soft fusion**: keep the original's low frequencies; at each pixel use whichever fine detail is stronger (original or AI) through a soft, smoothed weight. Lashes, lids and lip lines sharpen while skin texture (pores, marks) stays. Plain replacement smoothed the skin like a beauty filter, which is not acceptable for a clinic.
- Feature mask: an ellipse on eyes-to-lips (`plate_rx` 0.19, `plate_ry` 0.20); hair excluded, because the model paints hair like oil.
- **Flicker test before committing**: render 25 consecutive frames with and without the plates. The ratio of frame-to-frame change in the high-pass band must not exceed the ratio of detail gained. Results: hard fusion gave detail ×1.15 / change ×1.19 (fail); soft fusion gave ×1.10 / ×1.09 (pass).
- Never use GFPGAN, CodeFormer or RestoreFormer on real customers: they redraw the face.

# leevorá testimonial pipeline

Reproducible edit pipeline for single-take, phone-shot client testimonials: inspection, transcript,
audio cleanup, stabilised reframing, restrained grade, captions and end card.

**This repository is public. Footage, audio, stills, transcripts, caption text and exports are never
committed here.** `.gitignore` blocks them. Work in a private scratch folder and deliver files directly.

## What runs where

| Step | Tool | Licence |
|---|---|---|
| Inspect, cut, mux, encode | FFmpeg 6.1 | LGPL/GPL build |
| Transcript with word timings | faster-whisper 1.2.1 + Whisper large-v3, local CPU | MIT |
| Noise analysis, A/B scoring | numpy scripts in `scripts/` | — |
| Speech cleanup | FFmpeg pre-filter + DeepFilterNet3 0.5.6 (PyTorch 2.1.2 CPU, Python 3.11) | MIT / Apache-2.0 |
| Head tracking, stabilise, reframe, grade | `face_track.py`, `render_base.py` (numpy + Pillow) | — |
| Captions + end card | Remotion 4.0.543, transparent ProRes 4444 overlay | Remotion Licence: free for teams of up to 3, Company Licence above that |
| Fonts | Instrument Sans, Gloock | SIL OFL 1.1 (licence files alongside the fonts) |

Nothing is uploaded to a third-party service. Whisper and DeepFilterNet weights are downloaded once and run offline.

## Layout expected by the scripts

```
work/
  source_original/   the untouched camera file, chmod 444, with a .sha256
  scripts/           copy of ./scripts
  venvs/asr          python 3.13: faster-whisper
  venvs/dfn          python 3.11: torch==2.1.2+cpu torchaudio==2.1.2+cpu "numpy<2" deepfilternet==0.5.6 soundfile
  models/dfn/DeepFilterNet3/   config.ini + checkpoints/ (from the DeepFilterNet repository, models/DeepFilterNet3.zip)
  grade/             track.json, motion.json, stills
  project/           edl.json, client_data/ (phrases, props, SRT), remotion/
```

Install PyTorch from its CPU index first, then DeepFilterNet from PyPI (a single combined install fails on index ordering):

```bash
uv venv --python 3.11 venvs/dfn
uv pip install --python venvs/dfn/bin/python --index-url https://download.pytorch.org/whl/cpu "torch==2.1.2+cpu" "torchaudio==2.1.2+cpu"
uv pip install --python venvs/dfn/bin/python "numpy<2" deepfilternet==0.5.6 soundfile
uv venv --python 3.13 venvs/asr && uv pip install --python venvs/asr/bin/python faster-whisper==1.2.1
```

`transcribe.py` decodes the WAV itself and passes samples to Whisper, because faster-whisper 1.2.1's bundled decoder call is incompatible with PyAV 19.

## Workflow

1. **Lock the source.** Copy to `source_original/`, `chmod 444`, record `sha256sum`. Every later step reads it and writes elsewhere.
2. **Inspect.** `ffprobe` for duration, rotation, frame rate, colour tags and audio streams. Check frame timing, exposure stability (`signalstats`) and take stills. Note GPS metadata in iPhone files: strip it on export (`-map_metadata -1`).
3. **Audio analysis.** Extract the stereo AAC track to WAV, then `audio_analyse.py` reports hum and drone lines, band-by-band speech-to-noise, pause map and a rough reverb estimate. Use the *measured* lines in the notch filters; do not reuse another shoot's numbers.
4. **Transcript.** `transcribe.py <16k mono wav> <out.json> auto`. Run it on the original and on a cleaned version and compare: words that differ or score under 0.60 are the ones a person must confirm by ear (names and treatment names especially).
5. **Cleanup A/B.** `audio_chain.py <src> <out.wav> <attenuation limit dB> <target LUFS>`. `0` = original, level-matched. Limits of about 10–12 dB (gentle) and 18–20 dB (stronger) are the useful range; an unlimited setting gates to silence between words and sounds processed. `ab_metrics.py` scores candidates, but **a person chooses by ear** on headphones and a phone speaker.
6. **Edit decision list.** `examples/edl.IMG_5776.json` shows the format: source frame in/out per segment, zoom start/end, and where the face sits in frame.
   **Verify every cut point three ways before rendering:** the 5–10 ms loudness envelope, `probe_words.py` (isolated-window transcription either side of the cut), and a person listening.
   Two traps found on the first job: (a) a loud syllable is not necessarily the word you think it is, so an out-point placed "after the last word" from loudness alone can drop that word entirely; (b) a long-context transcription fills in plausible words that were cut off, and Whisper word times run up to 0.3–0.5 s early after a pause. Only short, isolated windows expose a clipped word.
7. **Track and motion.** `face_track.py` (set the head template position for the shot) then `render_base.py prep`. The renderer locks the crop to the background, so handheld sway is removed while her own movement stays natural.
8. **Grade stills first.** `render_base.py still ... --nograde` and without it, for each framing. Review before rendering video.
9. **Picture.** `render_base.py video ... --size 1080x1920` (or `2160x3840`) writes 10-bit Rec.709 ProRes 422 HQ.
10. **Voice.** `assemble_audio.py` cuts the mastered voice to the EDL with 12 ms fades at joins.
11. **Captions.** Write the phrase file (verbatim text, source seconds), then `build_captions.py` maps it to the edit timeline and writes Remotion props, word-level `Caption[]` JSON and an SRT.
12. **Overlay.** In `remotion/`: `npm install`, `npx remotion browser ensure`, then
    `npx remotion render src/index.ts Overlay out/overlay.mov --props=<props.json> --color-space=bt709`.
    The logo is generated from the client's own vector artwork with `logo_to_svg.py` into `remotion/public/leevora-logo-ivory.svg`; it is never redrawn.
13. **Composite and encode.** `finish.sh <base.mov> <overlay.mov> <mix.wav> <out> social|master <end-card seconds>` overlays the ProRes 4444 file on the graded picture, muxes the audio, tags Rec.709 and strips metadata. `social` writes 1080×1920 H.264 + AAC. `master` writes ProRes 422 HQ, then a compact 10-bit HEVC from it (one-pass x265 with the overlay filter is several times slower on four cores).
14. **Music.** `add_music.sh <video> <voice stem> <music file> <out>` sets the bed about 14 dB under the voice, ducks it further under speech with a slow release, lifts it under the end card and fades it out. The picture is stream-copied. Use only a track whose licence covers the intended use (organic and paid).
15. **QC before delivery.** One frame from every caption page; caption start against speech onset; loudness and true peak; skin tone sampled in every segment; frame-to-frame background movement; end-card colours against the brand values; container metadata empty; re-transcribe the final mix as a whole and in isolated windows.

## v2 look and sound (what changed after the first cut was rejected as too flat)

The first cut followed "restrained" too literally: a grade nobody could see, a light denoise, timid zooms, boxed captions, no music. v2 keeps the same honesty rules and raises the impact.

- **Voice.** `enh_clearvoice.py` (ClearVoice `MossFormer2_SE_48K`, Apache-2.0) after the hum pre-filter, then expander, body/presence/air EQ and 3:1 compression. Measured against the first cut: noise floor about 22 dB lower, pauses about 6 dB drier, word accuracy unchanged.
  - **Do not use a generative enhancer without checking the words.** `enh_resemble.py` (Resemble Enhance) produced a studio-dry sound and rewrote her speech into different words. `asr_batch.py` compares every candidate against the reference transcript; run it on anything that re-synthesises speech.
  - DeepFilterNet at 30 dB dries the room further but smears quiet consonants. Two-microphone WPE and `dereverb.py` added nothing measurable on this recording.
  - Room colouration during speech (distance from the phone) is not removable without re-synthesis. A lavalier or a phone within arm's reach is the real fix at the shoot.
- **Music.** `music_screen.py` shortlists instrumental tracks by measurable properties; `add_music.sh` sets the bed about 20 dB under the voice. Measure the result with the stems aligned by cross-correlation: the limiters add about 10 ms, and a naive subtraction gives nonsense.
- **Picture.** `render_base.py` now takes eased zoom keyframes per segment (`"zoom": [[source_frame, scale], ...]`) and a richer look in the edit list: warmer balance, stronger curve, split tone, vignette, luma-only sharpening and clarity, a soft bloom on the lights, fine grain. See `examples/edl_v2.IMG_5776.json`.
  - Avoid a same-size cut where material was lifted: change shot size by 15% or more across the join.
- **Type.** Gloock for the accent words, Instrument Sans for the rest, words arriving in sequence, a soft scrim and glow instead of a box. Check accent colours over the brightest object in frame, not just the average.

## Per-shot parameters to revisit

- `audio_chain.py`: `PRE` notch frequencies and high-pass corner, `FINISH` EQ.
- `face_track.py`: template centre and size for the reference frame.
- `render_base.py`: face size constants used for the feathered masks; grade values live in the EDL.
- `remotion/src/brand.ts`: colours. Confirm against the current brand book.
- Proper nouns (staff names, treatment names): speech recognition is not reliable on these in a noisy room. Leave an unconfirmed name out of burned-in captions until a person confirms it.

## Rules this pipeline follows

- No beauty filter, skin smoothing, face reshaping or generated face/voice. The only local picture adjustment is a soft, tracked exposure lift on the face and a slight dim of the surroundings.
- Captions are verbatim. No claims, names, treatments or calls to action are added that are not in the recording or the brief.
- Reframing stays at or below about 155% of this 4K source for a 1080×1920 export; beyond that the face goes soft.

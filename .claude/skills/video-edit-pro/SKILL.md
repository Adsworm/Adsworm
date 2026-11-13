---
name: video-edit-pro
description: Edit real footage (talking heads, client testimonials, UGC, Reels/Shorts ads, interviews) to a premium, human-edited standard with Claude Code. Covers intake, local transcription, cut planning, voice cleanup, stabilised reframing and push-ins, colour grade and dehaze, optional AI face-detail restoration, branded captions in Remotion, licensed music, QC and delivery. Use it whenever someone hands over a video file or link and asks to edit, clean, grade, caption, re-edit, fix quality, match a team's caption style, or build variants. Also routes to the installed video-use, rea-video, video-shotcraft, openmotion and moviepy tools when they fit better.
---

# Video Edit Pro

A complete editing method for real footage, assembled from a delivered client testimonial (three rounds of client feedback), five open-source video-agent projects, and research on creators who edit with Claude Code. Every rule here was either measured on real footage or learned from a mistake that reached a client. Read the reference file for a stage before you work on it.

## The non-negotiables

1. **The original never changes.** Copy it to `source_original/`, `chmod 444`, record `sha256sum`. Re-verify the checksum before every final render.
2. **Look, measure, then decide.** For any picture or sound complaint, isolate the cause with an ablation (render each processing stage separately and measure) before you change anything. "Hazy" turned out to have four separate causes, and two of them were our own processing.
3. **The client's words are sacred.** Captions are verbatim. Never invent, reorder inside a sentence or "improve" a quote. Take proper nouns (staff names, treatments) from client material (their earlier edits, website, documents), never from speech recognition alone.
4. **No generative change to people.** Do not use face-restoration models (GFPGAN, CodeFormer, RestoreFormer) or generative speech enhancers on testimonials, clinics or ads. They change skin, features or words. Allowed: deterministic processing, and Real-ESRGAN-general detail **fused** so the original texture is kept (see `references/03-picture.md`).
5. **Cuts are verified three ways:** a 5–10 ms loudness envelope, isolated-window transcription either side (`scripts/probe_words.py`), and a person listening. A loud syllable is not proof of the word you expect. One out-point was placed on "great" instead of "work" and nearly shipped.
6. **Nothing leaves the machine without explicit approval.** No uploads to ElevenLabs, Adobe Podcast, Higgsfield, VLM APIs and so on unless the user approves that exact upload. Local alternatives exist for every step.
7. **Public repositories never get client media**: no footage, audio, stills, transcripts, caption text or exports. Keep them in the scratchpad or a private location and hand them over as files.
8. **Ask → confirm → execute → self-review → deliver.** Show a transcript, a plan, an audio A/B, grade stills and a 15–20 s preview before rendering the full piece, unless the user has already approved the look.

## Workflow

| Stage | Do | Read |
|---|---|---|
| 0. Setup | `bash setup/bootstrap.sh <workdir>` (idempotent; reports what it installed) | `references/00-setup.md` |
| 1. Intake | ffprobe (rotation, VFR, colour, extra audio streams, GPS tags), loudness, noise spectrum, exposure over time, stills, contact sheet | `references/01-intake.md` |
| 2. Transcript | faster-whisper large-v3 locally, word timestamps, several passes, flag low-confidence words | `references/01-intake.md` |
| 3. Plan | Hook choice, edit decision list in source frames, framing per segment, caption pages, music plan | `references/04-cut-motion.md` |
| 4. Voice | Measure hum lines → notch → MossFormer2 (ClearVoice) → EQ/compression → loudness. Score candidates with `asr_batch.py`. | `references/02-audio.md` |
| 5. Picture | Track the face, lock the crop to the background, eased zoom keyframes, dehaze → WB → curve → glare control → face light → detail. AI detail plates are optional. | `references/03-picture.md` |
| 6. Captions & brand | Remotion overlay rendered to transparent ProRes 4444, Rec.709. Two ready systems: editorial (serif accents) and two-tier (Inter Tight white/gold). | `references/05-captions-brand.md` |
| 7. Music & mix | Licensed instrumental, bed about 20 dB under the voice, swell under the end card, −14 LUFS | `references/06-music-mix.md` |
| 8. QC & deliver | Frame check of every caption, sync, loudness, flicker, crop bounds, metadata, word-accuracy re-transcription; then social + master + SRT + stems + project | `references/07-qc-delivery.md` |

Tool routing (when another installed tool is the better choice): `references/08-tools.md`.
Lessons learned and the mistakes behind them: `references/09-lessons.md`.
Research on creators (MoSidd and others), and how to add transcripts: `references/10-research.md`.

## Quick start for a new job

```bash
W=$SCRATCH/job && mkdir -p $W/source_original && cp <file> $W/source_original/ && chmod 444 $W/source_original/*
bash .claude/skills/video-edit-pro/setup/bootstrap.sh $W        # venvs + models into $W (once per machine)
SK=.claude/skills/video-edit-pro/scripts
python3 $SK/audio_analyse.py <mono16.wav>                         # noise character, pauses, SNR
$W/venvs/asr/bin/python $SK/transcribe.py <16k.wav> words.json auto
python3 $SK/face_track.py <src> track.json && python3 $SK/render_base.py prep <src> $W/grade
python3 $SK/render_base.py still <src> $W/grade edl.json <frame> <segment> look.png   # grade stills first
python3 $SK/audio_chain.py <src> voice_all.wav 12 -16            # or the MossFormer2 chain in 02-audio.md
```

Then follow the workflow table. The edit is driven by one JSON edit list (`edl.json`): segments in source frames, zoom keyframes, face position and the grade. See `references/04-cut-motion.md` for the format.

## Defaults that held up on the first job (change them when the material says so)

- Vertical 1080×1920 social export: H.264 High, CRF 17, maxrate 16M, AAC 256k, −14 LUFS, true peak ≤ −1 dBFS, metadata stripped.
- Master: ProRes 422 HQ (composited once), plus 10-bit HEVC derived from it.
- Shot sizes: wide around 1.04–1.10, medium 1.30–1.40, tight 1.45–1.55 of a 4K portrait source. Change shot size by at least 15% across any non-contiguous join.
- Captions centred at 69–72% of frame height, 1–2 lines, accent colour on 1–3 words per page, soft dark glow instead of a box.
- Music bed about 20 dB under the voice during speech, rising about 7 dB under the end card, 1.5 s fade.

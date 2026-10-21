---
name: video-editing-pipeline
description: Footage to Meta-ready ads — cutdowns, 9:16 reframes, captions, ducking, loudness, AI B-roll via Higgsfield/fal/Runway. Use when the job starts from footage.
---

# Video Editing Pipeline

Footage jobs are edits, not motion jobs. Cut the story first, then add coded motion on top.

## Route the job

| Input | Tool | Notes |
|---|---|---|
| Talking head, podcast, UGC, interview | **video-use** skill (browser-use/video-use) | Cuts filler words, grades, burns subs, self-evaluates. Needs an ElevenLabs key |
| Any trim, reframe, caption, concat or loudness job, headless | **ffmpeg recipes** (`references/ffmpeg-recipes.md`, all tested) or the **Kinocut MCP** | Works in cloud containers |
| Fine cut, grade, finishing (desktop) | DaVinci Resolve MCP or Premiere Pro MCP | Needs the desktop app, so it won't run headless |
| Need B-roll, lifestyle, product-in-world, people | Gen-AI: Higgsfield MCP (`ads_studio_generate`, product photoshoot), fal, Runway (also proxies Kling/Veo/Seedance), Google Veo | Prompt "no text in frame" and add type in code. Sora's API was shut down in Sept 2026 |
| Avatar, UGC presenter, localization, lip-sync | HeyGen MCP, `fal-lip-sync` | Disclose AI presenters where the platform or law requires it |
| Motion overlays on footage | `remotion-ad-kit` with `backgroundVideo`, or a transparent ProRes 4444 overlay | Keeps copy editable across variants |

## Standard footage flow

1. **Ingest.** Make a contact sheet of every source (recipe 12) and read it before planning cuts.
2. **Transcript.** Extract 16 kHz mono WAV (recipe 10), then run whisper.cpp or ElevenLabs STT to get word timestamps. Write an `.srt` file.
3. **Paper edit.** Choose lines from the transcript to build `edit.md`: hook (first 2 s), problem, proof, offer, CTA. Cut on words, not on time.
4. **Cut.** Run video-use or the recipes (trim 3, concat 4, speed 8). Use J/L cuts for natural VO.
5. **Reframe** for each placement. Re-frame on the subject; use a crop (2) or a blurred fill (1). Never letterbox in Reels.
6. **Captions.** Burn them in (5), or use Remotion `@remotion/captions` for word-highlight styles. Keep them in the safe zone.
7. **Sound.** Duck music under VO (6), then normalize to −14 LUFS (`meta-delivery-qa`).
8. **Motion layer.** Add the kinetic hook and end card with `remotion-ad-kit` over the cut (`backgroundVideo`).
9. **QA and deliver** with `meta-delivery-qa`.

## AI footage prompt pattern (Higgsfield / fal / Runway)

> [subject + action], [setting], [lighting], [camera: lens, move], [palette words from brand.json], vertical 9:16, 5 s, photoreal, no text, no logos, no watermark

Generate 3–4 takes, pick by contact sheet, and trim to the cleanest 3–5 s. AI clips degrade after about 5 s.

## Rights

Log every clip's source, the generating model and its terms, and every music track license in `RIGHTS.md` (see `meta-delivery-qa`).

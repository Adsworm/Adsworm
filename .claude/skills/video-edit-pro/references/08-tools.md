# 08 · Tool routing

Installed and inspected on the first job (licence, dependencies, install hooks, network calls). Clone into a scratch folder, read before running, and keep each Python tool in its own venv.

| Tool | Licence | Use it for | Do not use it for / cautions |
|---|---|---|---|
| **This skill's scripts** | (ours) | Single-take testimonials, interviews, UGC; anything needing a precise grade, reframing, captions and QC | — |
| **video-use** (browser-use/video-use) | MIT | Multi-take raw footage: filler and silence removal, picking the best take per beat, 30 ms fades, self-eval at every cut, `project.md` memory | Its transcription uploads audio to **ElevenLabs** (API key). For client audio, use local Whisper and feed word JSON instead. Its hard rules (subtitles last, per-segment extract, output-timeline SRT) are adopted here. |
| **rea-video** (JuneYaooo/rea-video) | Apache-2.0 | Reverse-engineering a **reference** edit: shots, caption timeline, packaging, music BPM; produces VIDEO.md | Without a VLM it misjudges live footage as "AI" (it called a phone testimonial 71% AI). Use it for timeline and packaging data, then review frames yourself (`rea-video review` / `apply-review`). VLM keys send frames to a third party: ask first. |
| **video-shotcraft** (Vincentwei1021) | Apache-2.0 | Product and SaaS promos from screenshots: shot-card library, Remotion recipes, beat sync, SFX search; JianYing export | Not for talking heads. |
| **OpenMotion** (nexu-io) | Apache-2.0 | Recreating a reference social video as an HTML/Remotion-style template project with Motion.md; Studio for timing edits | It has PostHog telemetry (off unless enabled). Run with `DO_NOT_TRACK=1 OPENMOTION_TELEMETRY=0`. Its generative models (Seedance, Suno, Nano Banana) need the user's own keys and upload content. |
| **moviepy** 2.x | MIT | Quick scripted assemblies, prototypes, programmatic text and composites in Python | Slower than ffmpeg. Not for final colour-critical renders (it does not manage Rec.709 ranges). |
| **Remotion** + official skills (`npx remotion skills add`) | Free for teams ≤3; Company Licence above | Captions, titles, end cards, motion graphics; transparent ProRes 4444 overlays | Always pass `--color-space=bt709`. |
| **FilmCraft / EffectCraft** (storytold, alpha) | see repo | Premiere/AE-style editing through an MCP server (650+ commands: grade, denoise, loudness, captions) | Alpha software, not yet tested here. Evaluate before client work. |

Decision shortcuts:
- One take, premium polish → this skill.
- Many takes or long raw footage → video-use for the cut, then this skill for picture, sound and captions.
- "Make it like this reference" → rea-video to decode the reference, then build with this skill (real footage) or OpenMotion or shotcraft (motion graphics).
- Pure motion graphics / explainer (MoSidd style) → Remotion skills plus the motion rules in `04-cut-motion.md` and `10-research.md`.

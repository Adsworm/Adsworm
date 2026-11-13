# 10 · Creator research and how to extend this skill

## MoSidd (`@mo-sidd`, "Ex-Netflix Strategist")
Full notes: `research/mosidd-notes.md` (16 videos indexed from descriptions and chapters). Transcripts could not be fetched: YouTube blocks cloud IPs (`HTTP 429`, "Sign in to confirm you're not a bot").

What carries over:
- **Voiceover/line-first storyboarding.** Each spoken line becomes a scene with its own asset list and a 2–3 colour palette.
- **Decode a reference first** (the rea-video step), then build.
- **Few, spec-like prompts:** 1–6 per piece, each written like a spec (format, timing, palette, fonts, motion, exit criteria).
- **Cuts and motion land on the spoken word**, which needs word-level timestamps.
- **Always ease.** Prefer one continuous camera move to hard cuts. He uses push-in, pullback and portal-zoom transitions.
- **One shared finish across all scenes:** grain, paper or halftone, scanlines, vignette, tint. For premium real footage, keep the finish subtle and consistent.
- **Audio last:** voice, then music, then a foley/SFX pass.
- **Review loop:** check each scene in Remotion Studio, adjust by prompt, render 1080×1920.
- **Tools he links:** the Remotion Claude Code plugin; FilmCraft and EffectCraft (MCP editors); GSAP; Three.js; ElevenLabs.

He is strongest on motion graphics. For talking-head cutting, the more relevant creators are listed in `research/mosidd-notes.md` §6: Christian Peverelli, Matt Loui (CapCut skill), Jason Cooperson, kaye.creatives, Rourke, Eddie, Matt Wolfe, Lucas Leite and Brian Casel.

## Adding transcripts (run on your own computer, where YouTube allows it)
```bash
pip install yt-dlp
yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt \
  -o "%(upload_date)s_%(id)s_%(title).80s.%(ext)s" "https://www.youtube.com/@mo-sidd/videos"
```
If YouTube still blocks it, add `--cookies-from-browser chrome` (this runs locally; never paste cookies into a chat). Put the `.vtt` files in `research/transcripts/<creator>/` and ask Claude: "update video-edit-pro from the new transcripts". Claude should extract concrete techniques with timestamps into `10-research.md` and change the stage references only where a technique beats a measured result here.

## Updating this skill after every job
At the end of a job, append to `09-lessons.md` what the client rejected and why, and update defaults in the stage files only with measured evidence. Commit scripts and lessons; never commit client media or words.

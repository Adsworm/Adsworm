# Adsworm × Claude — working context (load this instead of re-reading old chats)

Updated 22 Oct 2026. Branch: `claude/funny-goldberg-b6mbmv`.

## Who / what
- **Adsworm** (adsworm.com), Delhi NCR performance agency. Founder **Aman Rai**, IG **@amanrai.official** (3.6K followers, 110 posts) + **@adsworm**.
- Brand: navy-black #080C14, cream #F0EEE8, blue #1B5EF7/#2B7BFF, gold #C8A96E · Bebas Neue + DM Sans · `brands/adsworm/brand.json`, verified claims in `brands/adsworm/claims.md` (280+ brands, since 2020, India/UK/UAE; never guarantee ROAS).
- Owner prefs: direct, premium, Hinglish chat OK. **Reels now in ENGLISH** (international audience). Token-frugal: cheap models for agents, short reports.

## What the data says (@amanrai.official, last 12 posts)
- AI-tool news reels win: "Video editing is about to change forever" 55K views/2.1K likes, "viral animated content…" 48K/1.4K.
- Meta-ads / clinic tips reels: 60–700 views. → Lead with AI/creative-tech news, use the agency lens (ad spend, CPA) as the differentiator.
- His face: thick full beard, voluminous swept-up dark hair, warm brown skin, **no glasses**, olive/earth hoodies & jackets. Refs: `/tmp/claude-0/face/pfp.jpg`, `p02.jpg` (Higgsfield media ids 1d907517…, 16fd5905…).

## Built so far
- `plugins/motion-studio/` Claude Code plugin (9 skills incl. `explainer-module`), `install.sh`, `docs/RESEARCH.md`.
- Reels: 01 (kinetic type, rejected: generic), 02 (dark cinematic, rejected: weird, unsynced), **03** `projects/adsworm-reel-03` (Hinglish two-avatar explainer, Diwali/Meta updates, 59 s, PASS). Feedback on 03: wants English, next-level motion, face-matched avatar, fluent voice, more original format.
- **04** `projects/adsworm-reel-04` = engine v2 pilot (English, flying camera over one canvas, THE ALGORITHM orb, face-matched Aman, synced captions, synth SFX), 39.5 s, spec PASS. Voice: one ElevenLabs v4 dialogue call (Aman = Holden 3c9d6053…, ALGO = Anika 4b2dc8f3… chosen for Indian-English accent — owner asked the female voice to sound Indian), silences capped 0.2 s + 1.06× tempo in `scripts/voice.py`. Owner verdict on 04: "bahut bekar, samajh nahi aaya" — too abstract (orb, flying camera, glitch, jargon). Do NOT reuse that format.
- **05** `projects/adsworm-reel-05` = reel 03's format in plain English: receipts card + Aman (3D) & Riya the brand owner (3D, Indian-English voice Anika) asking the client's questions. One-pass dialogue voice. 50.4 s, PASS. Rule going forward: clarity first — one idea per card, plain words, the second character asks what a client would ask.
- Pipeline (reel 03): `script/script.json` → `scripts/voice.py` (TTS + word timings → `timeline.json`, cache keyed by text hash, live `{days}` countdown, `--variant paid`) → Remotion (`src/reel/*`) → `scripts/render-reel.mjs` (−14 LUFS) → `check_specs.sh`.
- Render env: `REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`; run node scripts via `bash -c 'cd <project> && …'`.

## Voice findings (22 Oct)
- Choppy cause: per-line TTS calls + rate +40% + Hinglish code-switching + silence trim.
- **ElevenLabs v4 via Higgsfield** (`generate_audio`, model `elevenlabs_v4`, `dialogue:[{text,voice_type,voice_id}]`): whole conversation in ONE call, ~0.9 credits / 200 chars (~5 credits per reel). Word timings via faster-whisper `small` (word_timestamps). Presets tried: Holden (male) 3c9d6053…, Isla (female) 7367e919….
- Free fallback: edge-tts `en-US-AndrewMultilingualNeural` / `BrianMultilingualNeural` at +8%, whole paragraph per call.
- Best: clone Aman's own voice (Higgsfield `create_voice` widget, 1–2 min clean speech) → his voice in every reel.

## Motion upgrades to use (Remotion)
- Virtual camera over one infinite canvas (CSS 3D `perspective`, zoom/pan between "rooms"), `@remotion/motion-blur` CameraMotionBlur, `@remotion/paths` interpolatePaths morphs, rebuilt UI in React instead of flat screenshots, animated counters, depth parallax.

## Higgsfield
- ~1,100 credits. nano_banana_pro character sheets ~2 credits each; avatars keyed with `scripts/avatars.py` (green bg).

## Rules
- Facts only with receipts in `script/sources.md`. Ad spend / campaign activation only on owner's explicit go (create paused).
- Commit trailers: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` + `Claude-Session: https://claude.ai/code/session_01NzyjL8BD95hveymJMb1FZJ`.

## Content pipeline (22 Oct 2026, owner-requested)
Research agent → concept/script agent → approval agent (facts+strategy) → production director (retention, delivery, sound) → build. Files per day in `docs/pipeline/<date>/` (01-research, 02-concepts, 03-approval, 04-director, reel-*.final.json, POSTING.md).
Engine = `projects/adsworm-reel-06` (data-driven: sections[].views in script.json, item types in `src/reel/views.tsx`; copy the project per reel, drop final JSON in `script/script.json`, generate the dialogue in ONE ElevenLabs v4 call → `script/dialogue.mp3`, `python3 scripts/voice.py`, `node scripts/render-reel.mjs --no-voice`).
22 Oct output (agency @adsworm): reel-06 "Ads feel expensive this October" (OCTOBER), reel-07 "Meta product browsing from 28 Oct" (BROWSE).

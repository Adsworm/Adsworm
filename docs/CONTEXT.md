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

## Engine v3 (22 Oct, after owner feedback "no fun / conversation not clear")
`projects/adsworm-reel-08` (reel A) / `-09` (reel B). Learned from reference reel Det2rTBzoEq (`docs/playbook/REFERENCE-Det2rTBzoEq.md`) + research playbook (`docs/playbook/REEL-PLAYBOOK.md`):
teacher (Aman) + student who gets it wrong (Riya) as talking-head busts with lip-flap (`public/faces/*`, built by `scripts/faces.py` from AI-edited mouth frames), karaoke bubble captions (2–4 words), proof board that builds on spoken words (`views` with `word`, new items in `src/reel/board.tsx`), stickers, whip transitions, zoom-punch hook + thump, follow/share ending + wink.
Voice: ElevenLabs v4 dialogue with inline audio tags (`tags` per line; Higgsfield passes them through); `voice.py` keeps non-silent gaps (laughs). `python3 scripts/dialogue.py` prints the generate_audio params.

## Engine v4 + batch of 11 Nov 2026 (current: start here)
- **Engine:** `projects/adsworm-reel-10` = one engine, many reels (`reels/<slug>/script.json + dialogue.mp3 + sources.md`, `REEL=<slug>` on every script). Adds: listener reactions and pre-line faces (`react`, `pre`; frames aman `laugh surprised wink`, riya `shock laugh doubt worry`), sound played by visuals (`Sfx.tsx`, numpy-synthesized `public/sfx`), open-loop chip + payoff breath (`loop`, `payoff`), finished frame 0, pad ducking, generic board items (`headline scene chatThread aiChat clock plan`), free edge-tts draft (`draft_voice.py`), `qa_report.py`.
- **Skills:** `plugins/motion-studio` 1.1.0: `explainer-module` (v4 + `references/retention-rules.md`, `script-schema.md`), new `reel-pipeline`. Rulebook: `docs/playbook/EDITING-PSYCHOLOGY.md`.
- **Process that worked:** research agent → I write the scripts → independent approval agent (facts + edit) → free draft QA → paid voice (one call per reel, ~3.5 credits) → render. Never generate voice before approval.
- **Batch** (`docs/pipeline/2026-11-11/`, kit in `POSTING.md`): `black-friday-week` (FRIDAY, post by Sun 15 Nov), `chatgpt-ads` (CHATGPT), `late-replies` (REPLY). Next candidates from the research: "Stop touching your ads every day" (pressure-cooker analogy, Meta's 50-conversions receipt), "Boost is not a campaign", "Meta counts more sales from 12 Nov".
- If the worker restarts mid-call, check Higgsfield `transactions` before re-sending a paid generation.

## Hinglish reel + first-party data (12 Nov 2026)
- **Reel:** `reels/october-bleed` (Hinglish, keyword SETUP), files in `docs/pipeline/2026-11-12/` (`01-research.md`, `02-account-data.md`, `POSTING.md`). Owner's brief: "October bled, after Diwali performance is coming back; explain why, what Meta changed, how to structure".
- **What our accounts actually showed (18 accounts, anonymised, read-only pull):** cost per message enquiry rose Sep → Oct in 15 of 17 (median +16%), but CPM and cost per click did NOT rise (about −5%). Diwali week (1–8 Nov) was the peak (₹210 blended vs ₹147 Sep, ₹165 Oct); 9–11 Nov fell back to ₹164. So: say "enquiry mehngi" and "cost peak se neeche aayi hai" (13 of 16 accounts, three days); never "CPM went up", "back to normal" or "better than October". The independent approval pass (`03-approval.md`) caught a green "wapas ✓" stamp that implied recovery. Client names and account ids stay out of the repo.
- **Hinglish engine rules:** `"lang": "hi"`; `say` in Devanagari + English, `show` in Latin with the same word count per line; cues written against the Latin caption; Whisper `medium`, one pass on the raw audio, sound-skeleton alignment (`voice.py`). New board items `columns`, `formula`, actor `disc`. Details in `plugins/motion-studio/skills/explainer-module/references/script-schema.md`.
- **Voice:** same presets as the English reels (Holden, Anika) read Devanagari clearly: 128 of 130 words matched by Whisper. ElevenLabs Hindi came out slow (2.07 words/s), so `tempo` is 1.15; 130 words ran 56 s. Aim for ~120 words next time. Accent by ear is still unverified.
- **Gotcha:** `timeline.json` is built by `voice.py` from `script.json`; re-run it after any view change or the render shows the old board.

## Andromeda batch (13 Nov 2026)
- **Reels:** `reels/andromeda-2` (keyword ANDROMEDA, 50 s) and `reels/ad-is-targeting` (keyword TARGET, 53 s), both Hinglish. Files in `docs/pipeline/2026-11-13/` (`01-research.md`, `03-approval.md`, `POSTING.md` with the order for all six reels).
- **Findings to keep:** "Andromeda 2.0" is not a Meta name (Meta's 28 Oct 2026 post says "the next generation of Meta Andromeda"; "2.0" appears zero times). Meta: "no setting to switch on, no new campaign type to adopt, no migration to plan". No Meta page gives a number of ads; "one ad set", "30 ads" and "3 ads = 3 kinds of people" (from the owner's reference reel, @gabritataranni) have no Meta source. Any number of ads we say is "humari salaah".
- **Engine:** `src/reel/board3.tsx` adds `oldNew` (campaign structure old → new), `find` (find-in-page proof card), `truths` (true vs rumour save card). Headlines shrink with their longest line: keep each line ≤ 14 characters and use three lines instead.
- **Timing robustness (found on a draft):** in one pass Whisper skipped four whole lines, and `tighten` then cut the last line off. Now `voice.py` transcribes in ~18 s pieces, keeps audio up to the last loud sample, and writes the match rate; `qa_report.py` fails under 90% and walks every `…Word` / `…At` cue of any item.
- **Hook pattern that the research supports:** keep the scare word in line 1 ("Andromeda 2.0 aa gaya!") and pay it off with relief and a receipt. Calm myth-busting titles got hundreds of views; alarm titles got tens of thousands.


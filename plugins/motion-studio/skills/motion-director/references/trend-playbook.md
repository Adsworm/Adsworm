# Coded-motion trend playbook (researched 2026-10-21)

## How the wave unfolded
- **20 Jan 2026:** Remotion shipped Agent Skills. They passed 440K installs by August.
- **17 Apr 2026:** HeyGen open-sourced HyperFrames (HTML+GSAP → MP4, Apache-2.0). It has about 69k GitHub stars.
- **22 Sep 2026:** The Opus 5.5 "showreel" wave started. The most-cited single post did 1.98M views on X (@stephanlivera).
- **8 Oct 2026:** Anthropic launched **Claude Motion** in beta for Team/Enterprise. It turns prompts into code-built animation with MP4 export and uses no video model.

## Formats that perform on social right now
- **Showreel / launch film.** Kinetic type, UI broken into animated components, cut to the beat.
- **Apple-keynote product film.** One idea per beat, no crossfades, ambient idle instead of dead holds.
- **Vox-style collage explainer.** MoSidd, 234K views: https://www.youtube.com/watch?v=7wuYBfE131U
- **Prompt-to-website reveal / app demo.** UI recreated in code, not screen-recorded.
- **Kinetic charts and stat counters.**
- **Logo stings and lower-thirds.** Transparent ProRes 4444 for editors.

## Workflows worth copying
1. **Staged client-grade flow** (@0xCodila, 486K views):
   - Write `brief.md`, `style-guide.md` and `storyboard.md` with frame ranges, and review them before building.
   - Build as a registered composition.
   - Render a low-res preview and a contact sheet, then fix the 3 worst defects.
   - Do a sound pass, with QA capped at 3 rounds.
   - Make the vertical cut by *re-laying out* the approved film, not cropping it.
   - Save the process as a skill.
2. **Framework-free HTML**: `seek(t)` is a pure function of time.
   - Capture with Playwright using 6–8 sub-frames, and blend them with ffmpeg `tmix` for motion blur.
   - Find the BPM and the drop first, put SFX on measured peaks, and use `loudnorm` to hit −14 LUFS.
   - Source: https://github.com/hoodini/motion-in-code
3. **Hybrid finish** (Matt Loui, 98K views): render 4K in Remotion, then spend about 5 minutes in an NLE on chromatic edges, radial blur and whoosh/UI-pop sound.

## Hard truths
- **"15 minutes" is the tooling, not the craft.** Real client pieces took 1 to 12 hours of directing, and about 1 in 5 prompts needs a real fix (rushed timing, text collisions, type too small in vertical).
- **"$0" means the tools are free, not the tokens.** One measured 30-second job used about 59% of a Pro 5-hour window.
- **Out of scope:** organic or character animation, photoreal people, interview footage edits, and news-speed turnarounds.

## Pricing benchmarks (for positioning, as reported Oct 2026)
- **Freelance marketplaces:** $30–$500 per SaaS video. Mid-tier Fiverr gigs run $200–$400. One Upwork B2B demo was about $2,000.
- **Agencies:** $1,000–$8,500 for SaaS video, $1,500–$5,000 for kinetic typography. One studio quotes from $3,480 per 30 s.
- **Premium positioning:** don't sell "AI video". Sell variant velocity, meaning 12–40 on-brand variants per sprint with QA and naming wired to Meta reporting. That's the moat the $129 freelancers can't match.

## Study list
- **YouTube:** MoSidd, Matt Loui, Jason Lee, Andy Lo (9-phase workflow), Mauro Arredondo (an After Effects pro testing it), Maciej Dziuba (HyperFrames for editors).
- **X:** @twoclipping (zero), @aschapmann, @0xCodila, @charliejhills, @rexan_wong (his reverse-engineered workflows beat one-shot prompts).
- **Prompt libraries:** https://www.remotion.dev/prompts · https://hyperframes.heygen.com/prompting/examples.md · https://yuv.ai/motion

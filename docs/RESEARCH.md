# Coded motion, video editing and design tooling for a premium Meta ads agency

**Research date:** 2026-10-21.
**Method:** four parallel research passes covering frameworks, MCP connectors, skill marketplaces and the social/reels trend. Each pass used the vendors' READMEs and docs, the npm and PyPI registries, and the creators' posts.

**Source markers:**
- ⚠ means the claim could not be verified against a primary source.
- [mirror] means an X post read through a verbatim copy. X itself returned HTTP 402.

**Gaps in coverage:** Reddit blocked automated access, and Instagram reels are not indexed, so those two were not covered directly.

---

## 1. Verdict in one screen

**Core stack:**
- **Engine:** Remotion, with its official Claude Code plugin and a license if the team has 4+ people. HyperFrames is the Apache-2.0 second engine.
- **Motion engine and voice:** GSAP for motion. ElevenLabs for voice, SFX and music. whisper.cpp for captions. ffmpeg for conform.
- **Design and generation connectors:** Figma (remote), Canva, Adobe for creativity, fal, Higgsfield and HeyGen.
- **Desktop finishing:** the DaVinci Resolve or Premiere Pro MCP, plus After Effects for anything code can't do.

**What the market is missing,** and therefore what this repo builds:
- Deterministic Meta delivery QA
- Multi-client brand switching
- A production variant matrix wired to ad naming
- A motion critique rubric for ads
- Coded static ads
- A performance loop from Meta insights back into the next creative round

**Reality check on "15 minutes":**
- The tooling is fast; the craft still takes time. Client-grade pieces took 1–12 hours of directing.
- About 1 in 5 prompts needs a real fix.
- One measured 30-second job used 31.8M tokens over 54 minutes, about 59% of a Pro plan's 5-hour window. [mirror] https://www.ayautomate.com/resources/claude-opus-5-5-motion-graphics

---

## 2. Code-driven video frameworks

| Tool | What | Install | License | Maturity | Verdict |
|---|---|---|---|---|---|
| **Remotion** | React → MP4 | `npx create-video@latest --yes --blank my-video && cd my-video && npx remotion skills add` | Source-available. Free for ≤3 people, otherwise a Company License | `remotion@4.0.537` (2026-10-19), ~66k★, ~8M npm downloads/month | **USE** |
| Remotion Claude Code plugin | 12 skills: best-practices, create, markup, studio, render, captions, maps, saas, interactivity, docs, upgrade, multimedia | `claude plugin marketplace add remotion-dev/claude-code-plugin` then `claude plugin install remotion@remotion` | — | ~275 always-on tokens (measured) | **USE** |
| Remotion MCP | Docs only | — | — | **Deprecated**: "shut down no earlier than Aug 31 2026" | SKIP |
| **HyperFrames** (HeyGen) | HTML/CSS/GSAP → deterministic MP4, built for agents | `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes`. Also `npx hyperframes init` | **Apache-2.0**, no per-render fees | 0.8.184 (2026-10-21), ~69k★, near-daily releases | **USE** (second engine, license hedge). ~4.1k always-on tokens (measured) |
| GSAP + gsap-skills | Timeline engine; all plugins now free | `npm i gsap`; `npx skills add greensock/gsap-skills` | Standard no-charge license (revocable) | 3.15.0 | **USE** |
| Lottie / dotLottie | Vector micro-animation | `@lottiefiles/dotlottie-web`, `@remotion/lottie`; Creator MCP `npx -y @lottiefiles/creator-mcp@latest` | MIT runtime | — | OPTIONAL |
| Rive | State-machine animation | `@rive-app/canvas`, `@remotion/rive`; editor MCP early access | MIT runtime | — | OPTIONAL |
| Manim CE | Math and explainer animation | `uv add manim`; skill `npx skills add adithya-s-k/manim_skill` | MIT | 0.22.0 | OPTIONAL (explainers only) |
| Motion Canvas | Editor-centric | `npm init @motion-canvas@latest` | MIT | Last release Dec 2024 (dormant) | SKIP |
| Revideo | Motion Canvas fork | — | MIT | Docs now redirect to a commercial product | SKIP |
| Theatre.js | Timeline studio | — | Studio is **AGPL** | Development moved private | SKIP |
| Etro / Diffusion Studio / Twick / editly | Browser and JSON editors | — | GPL-3.0 / watermark-or-pay / no-resale / stale | — | SKIP |

**Remotion license detail.** Sources: https://www.remotion.dev/docs/license/faq and https://www.remotion.pro/license
- Headcount means all personnel, "regardless of whether they use the Remotion Software".
- Creators tier: $25 per seat per month. A seat covers someone using "agentic coding tools such as Claude Code".
- Automators tier: $0.01 per render, $100/month minimum. It covers programmatic `renderMedia()`, `npx remotion render` and Lambda.
- Enterprise: from $500/month.
- An agency delivering only MP4s counts only its own headcount. If the client runs the code, the two headcounts combine.

**Template-JSON video APIs** (an overflow lane for volume):
- Shotstack MCP: `claude mcp add --transport http shotstack https://mcp.shotstack.io`. From $39/mo.
- Creatomate MCP: `https://api.creatomate.com/mcp`. Credit-based; ⚠ prices didn't render on the pricing page.
- Plainly: drives After Effects templates by API, from $69/mo. Highest quality ceiling if you have AE designers.

**Rendering:** Remotion Lambda costs about $0.017–0.021 per minute of video in compute, with bandwidth and storage extra. Headless rendering has no GPU, so blur, 3D and particle scenes are slow.

---

## 3. MCP connectors

⚠ = Claude Code command inferred from the vendor's config rather than documented.
🖥 = needs the desktop app (won't run in a cloud container).

| Area | Server | Install | Verdict |
|---|---|---|---|
| Headless editing | **Kinocut** (ffmpeg, 203 tools) | `claude mcp add kinocut -- uvx --from kinocut kino --mcp` | **CORE** |
| NLE 🖥 | **DaVinci Resolve MCP** (3.7k★, v4.14.4) | `npx davinci-resolve-mcp setup` | **CORE** |
| NLE 🖥 | Premiere Pro MCP (leancoderkavy, 436 tools) | `/plugin marketplace add leancoderkavy/premiere-pro-mcp` → `/plugin install premiere-pro@premiere-pro-mcp` → `npx -y premiere-pro-mcp@1.24.3 --install-cep` | CORE for Premiere shops |
| Motion 🖥 | After Effects MCP (Dakkshin, 774★) | Build, then `npm run install-bridge`; run the panel in AE | OPTIONAL |
| 3D 🖥 | MCP for Blender (31.9k★) | `claude mcp add blender uvx mcp-for-blender` | OPTIONAL |
| Adobe cloud | Adobe for creativity (official, launched 2026-04-28) | Claude app connector. ⚠ `https://adobe-creativity.adobe.io/mcp` | CORE for resizes, Firefly and Stock. It does not drive the Premiere or AE timeline |
| Design | Figma remote (official) | `claude plugin install figma@claude-plugins-official` | **CORE** |
| Design | Canva (official) | ⚠ `claude mcp add --transport http Canva https://mcp.canva.com/mcp` | **CORE** for template autofill and MP4 export |
| Vectors | Recraft (official remote) | `claude mcp add --transport http recraft https://mcp.recraft.ai/mcp` | OPTIONAL |
| Stock + gen | Magnific (formerly the Freepik API) | `claude mcp add --transport http magnific https://mcp.magnific.com` | OPTIONAL (strong) |
| Gen media | **fal** (official) | `claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay` | **CORE** |
| Gen media | Higgsfield | CLI `npm i -g @higgsfield/cli`. ⚠ MCP `https://mcp.higgsfield.ai/mcp` | OPTIONAL (ad-specific workflows) |
| Gen media | Runway | The skills plugin `runway-api@runway-dev`. Proxies Gen-4.5, Kling 3.0, Veo 3.1 and Seedance | OPTIONAL |
| Avatars / UGC | **HeyGen** (official) | `claude mcp add --transport http heygen https://mcp.heygen.com/mcp/v1/` | **CORE** |
| Voice | ElevenLabs hosted | ⚠ `https://api.elevenlabs.io/v1/mcp`. TTS and agents only; the local server was archived 2026-08-20 | OPTIONAL. Use skills for SFX and music |
| Voice / music | Hedra | `claude mcp add --transport http hedra https://mcp.hedra.com` | OPTIONAL |
| **Dead** | Sora API (shut down 2026-09-24), Luma AI MCP, Spline MCP | — | SKIP |

**Works headless:** Kinocut, fal, Figma remote, Canva, Adobe, HeyGen, Higgsfield, Runway, Recraft, Magnific and ElevenLabs. The OAuth servers need a one-time login; use `claude mcp login <name> --no-browser` on remote boxes.

**Needs a desktop app or an open tab:** Resolve, Premiere, After Effects, Photoshop, Illustrator, Blender, Penpot and Lottie Creator.

---

## 4. Skills and plugins worth installing

**Warning:** skills.sh install counts are gamed. Some forks show 500k–830k installs against 14 at the source. Trust stars and reading the code instead.

| Skill / plugin | Install | Verdict |
|---|---|---|
| anthropics/skills: frontend-design, canvas-design, algorithmic-art, theme-factory | `/plugin marketplace add anthropics/skills` | MUST (several are already synced on this account) |
| remotion-dev (plugin) | see §2 | MUST |
| heygen-com/hyperframes | see §2 | MUST, if you use HTML/GSAP |
| greensock/gsap-skills | `npx skills add greensock/gsap-skills --skill gsap-core gsap-timeline gsap-plugins gsap-performance` | MUST with HyperFrames |
| LottieFiles/motion-design-skill | `npx skills add LottieFiles/motion-design-skill` | MUST (cheap principles layer) |
| elevenlabs/skills | `npx skills add elevenlabs/skills --skill text-to-speech sound-effects music speech-to-text dubbing` | MUST |
| Leonxlnx/taste-skill (100k★) | `npx skills add Leonxlnx/taste-skill --skill design-taste-frontend` | MUST |
| emilkowalski/skills (48k★) | `npx skills add emilkowalski/skills --skill animate review-animations animation-vocabulary apple-design` | MUST (filtered: the repo also ships Swift and toast skills) |
| pbakaus/impeccable (84k★) | `npx impeccable install` | NICE (anti-slop detectors) |
| browser-use/video-use (29.5k★) | Clone, then symlink into `~/.claude/skills`, then `uv sync` | MUST for footage cutdowns |
| higgsfield-ai/skills | `--skill higgsfield-generate higgsfield-product-photoshoot higgsfield-brandkit` | NICE |
| runwayml/skills | `claude plugin marketplace add runwayml/skills` then `claude plugin install runway-api@runway-dev` | NICE |
| calesthio/OpenMontage (70k★) | Full production workspace | Mine its pipelines; not a drop-in |
| iart-ai/ad-video-skills, charlie947/motion-graphics-skills | `npx skills add …` | NICE, but early (v0.1) |

**Packaging facts used for this repo** (from code.claude.com docs):
- `marketplace.json` lives at `.claude-plugin/` in the repo root. Each plugin has its own `.claude-plugin/plugin.json`, and skills live at `skills/<name>/SKILL.md`.
- `SKILL.md` `name` must be `[a-z0-9-]` and match the folder name.
- `description` plus `when_to_use` is truncated at 1,536 characters.
- `${CLAUDE_SKILL_DIR}` resolves inside the skill body.

---

## 5. The social trend: what is actually happening

**Timeline:**
- **20 Jan 2026:** Remotion Agent Skills launched. They reached 440K+ installs by August.
- **17 Apr 2026:** HyperFrames open-sourced.
- **22 Sep 2026:** Opus 5.5 released, and the "showreel" wave started. The top post did 1.98M views on X (@stephanlivera). [mirror]
- **8 Oct 2026:** Anthropic launched **Claude Motion** in beta for Team and Enterprise: prompt → code-built animation → MP4, with no video model. https://claude.com/resources/articles/dashboards-and-motion

**Workflows that produce client-grade work:**
1. **Staged:** brief, style guide and storyboard with frame ranges, approved before building. Then build, review a low-res contact sheet, fix the 3 worst defects, do a sound pass, cap QA at 3 passes, and re-lay out (not crop) for vertical. @0xCodila, 486K views. [mirror] https://youmind.com/landing/x-viral-articles/monetize-ai-motion-design
2. **HyperFrames:** the agent interviews you into `BRIEF.md`. Run `npx hyperframes lint && check` before rendering, because it catches overflow, collisions and contrast problems. https://hyperframes.heygen.com/guides/prompting
3. **Framework-free HTML:** a pure `seek(t)` function, Playwright frame capture with sub-frame motion blur, a beat map before animating, and −14 LUFS. https://github.com/hoodini/motion-in-code
4. **Hybrid finish:** Remotion 4K render, then about 5 minutes in an NLE for chromatic edges, radial blur and sound design. Matt Loui, https://www.youtube.com/watch?v=Ll45R_Z8tQc

**Tips with consensus:**
- Supply real assets and approved claims.
- Specify size, fps and frame ranges.
- Ban the template look explicitly.
- Stay deterministic: no random numbers, timers or CSS transitions.
- Keep holds alive with an ambient idle.
- Bundle fonts locally.
- Avoid `filter: blur()` on big layers, which makes renders 5–10× slower.
- Iterate on stills.
- Check on a phone, muted.

**Limitations:**
- Character and organic animation.
- Photoreal people (use generative video instead).
- Interview and footage-heavy edits.
- News-speed turnarounds.
- One-prompt output reads as "mid".

**Pricing benchmarks:**
- Marketplaces: $30–$500 per SaaS video, $200–400 for mid-tier Fiverr gigs, about $2,000 for an Upwork B2B demo.
- Agencies: $1,000–8,500 for SaaS video and $1,500–5,000 for kinetic type (⚠ snippet-level).
- Premium positioning: sell variant velocity with QA and reporting, not "AI video".

**Creators to study:**
- **YouTube:** MoSidd (Vox-style, 234K), Matt Loui (98K), Jason Lee (91K), Andy Lo (9-phase workflow, 62K), Mauro Arredondo (an After Effects pro testing it), Maciej Dziuba (HyperFrames for editors).
- **X:** @twoclipping, @aschapmann, @0xCodila, @charliejhills, @rexan_wong.
- **Prompt libraries:** https://www.remotion.dev/prompts · https://hyperframes.heygen.com/prompting/examples.md · https://yuv.ai/motion

Verbatim prompts with attribution are in `plugins/motion-studio/skills/motion-director/references/prompt-library.md`.

---

## 6. Could not verify

- Latest GitHub release tags (the GitHub API was blocked during research).
- Live Creatomate prices, and Rive and Lottie Creator plan prices.
- The HyperFrames hosted-render credit cost.
- Rendervid's repository.
- The Claude Code commands for the Adobe, Descript, ElevenLabs-hosted and Runway generation MCPs (inferred from their configs).
- The "6M views" Remotion demo figure and the "$5k–15k studio price" claim (secondary sources only).

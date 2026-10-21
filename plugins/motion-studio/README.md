# Motion Studio: Claude Code skills for coded motion and Meta ad video

Motion Studio takes an ad from brief to delivery. It covers motion graphics, video editing, static ads and creative testing for a premium Meta ads agency. Everything here was built and verified in a headless Linux container in October 2026.

## Install

**Install everything**, using the profile installer from a clone of this repo:

```bash
git clone https://github.com/Adsworm/Adsworm && cd Adsworm
./install.sh --dry-run core html     # see exactly what will run
./install.sh core                    # recommended start
```

**Install only this plugin**, from inside Claude Code:

```
/plugin marketplace add Adsworm/Adsworm
/plugin install motion-studio@adsworm
```

**Install the skills into other agents** (Cursor, Codex and so on) with `npx skills add Adsworm/Adsworm`.

Requirements: Claude Code, Node 22+ and ffmpeg. The `editing` profile also needs git and uv.

## Profiles and what they cost

Every installed skill sits in Claude's context on every message. Install the profiles you use and nothing else. The table shows the always-on token cost, measured with `claude plugin details`.

| Profile | Installs | Always-on |
|---|---|---|
| `core` | motion-studio (8 skills) · Remotion official plugin (12) · LottieFiles motion-design · ElevenLabs TTS/SFX/music/STT/dubbing | ~645 + ~275 tok, plus skill descriptions |
| `html` | HyperFrames plugin (21 skills) · GSAP core/timeline/plugins/performance | **~4.1k tok** for HyperFrames: disable it between jobs |
| `taste` | design-taste-frontend · Emil Kowalski animate/review/vocabulary/apple-design | small |
| `editing` | video-use (footage cutdowns) · Kinocut MCP (headless ffmpeg) | MCP tools load on demand |
| `genai` | Runway skills · Higgsfield generate/photoshoot/brandkit · fal MCP | MCP tools load on demand |
| `desktop` | prints setup steps for the DaVinci Resolve, Premiere Pro, After Effects and Blender MCPs | — |

Third-party repos are installed through a filter. For example, Emil Kowalski's repo has 15 skills, but only the 4 motion ones are installed. Without the filter, `write-swift` and `ask-sonner` would end up in your context.

## Skills

| Skill | Job |
|---|---|
| `motion-director` | Entry point: brief → engine choice → storyboard → build → QA → delivery, with token-budget rules |
| `remotion-ad-kit` | A production Remotion template. One prop set renders 9:16, 4:5, 1:1 and 16:9 video plus static PNGs. Includes a footage background lane, QA sheets and variant batches |
| `motion-taste` | Easing, timing and typography rules, a list of banned effects, and a 12-point critique rubric |
| `meta-delivery-qa` | `check_specs.sh` (PASS/WARN/FAIL per placement), tested fix commands, naming, and the handoff package |
| `ad-variant-matrix` | Hooks × offers × CTAs × formats, rendered with Meta-ready names and a `manifest.csv` |
| `brand-motion-system` | One `brand.json` per client, compiled into Remotion, HyperFrames, GSAP and CSS settings |
| `video-editing-pipeline` | Footage routing plus 14 tested ffmpeg recipes (reframe, captions in the safe zone, ducking, LUT, overlays) |
| `creative-performance-loop` | Meta hook rate, hold rate and CPA per ad, mapped back to each axis, and written into the next matrix. Read-only by default |

Start a job with: `/motion-studio:motion-director <brief>`.

## The Remotion ad kit (verified)

- A 12.6 s 1080×1920 ad renders in **44.5 s** on 4 CPU cores. The 4:5 version takes 32.7 s.
- Output is H.264 High, yuv420p, BT.709, CRF 18. `check_specs.sh` passes it.
- Fonts are bundled locally under the SIL OFL license, so renders never depend on Google Fonts loading.
- Bugs caught by its own QA loop while it was being built, all fixed:
  - stat rows wrapping in 1:1
  - full-range `yuvj420p` output
  - `<Freeze>` not settling statics
  - `--dry-run` being swallowed by npm

## Licensing: read this before agency use

- **Remotion** is free only for organisations of **3 people or fewer**, and that headcount counts everyone, not just users. Above that you need a Company License: Creators at $25 per seat per month, or Automators at $0.01 per render with a $100 monthly minimum. Scripted batch renders count as automation. Set `REMOTION_LICENSE_KEY`. Get written confirmation from Remotion for your setup.
- **HyperFrames** is Apache-2.0 with no render fees, which makes it the hedge.
- **GSAP** is free for commercial use under a revocable no-charge license.
- **ElevenLabs** needs a paid plan for commercial audio.
- **Music, stock and AI-model output** each have their own terms. Log them in `RIGHTS.md`.

Full research, with sources, is in [`docs/RESEARCH.md`](../../docs/RESEARCH.md).

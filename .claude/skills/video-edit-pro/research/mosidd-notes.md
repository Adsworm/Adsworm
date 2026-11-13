# Research notes: MoSidd (YouTube) on AI-agent video editing with Claude Code

Compiled 2026-11-13. Read-only research. For use in writing a Claude Code skill for editing talking-head, testimonial and ad videos.

## 0. Read this first: what these notes can and cannot tell you

**The channel.** The handle `@mosidd` is a different, empty channel (1 subscriber, "This channel doesn't have any content"). The creator is:

- **MoSidd, handle `@mo-sidd`**: https://www.youtube.com/@mo-sidd
- Channel ID UC1DOBzuJajJjhpj4e3EVQlQ, about 21.4K subscribers.
- Channel tagline: "Ex-Netflix Strategist sharing the secret sauce to becoming an AI Creative." Video descriptions sign off as "MoSidd | AI Made Easy".
- His Skool profile gives his name as Mo Siddique (skool.com/@khal-siddique-9947).

**Transcripts could not be obtained (0 of 16).** YouTube blocks this cloud IP:

- yt-dlp 2026.10.26 (`--skip-download --write-auto-subs --sub-langs "en.*,hi.*"`), tried twice on two videos:
  - `WARNING: [youtube] zCuthqXIAcg: Unable to download webpage: HTTP Error 429: Too Many Requests`
  - `ERROR: [youtube] zCuthqXIAcg: Sign in to confirm you're not a bot. Use --cookies-from-browser or --cookies for the authentication.`
  - The same errors came back for dBakc0BdHjY. The log is in `raw/ytdlp_retry_error.txt`.
- youtube-transcript-api: `IpBlocked: Could not retrieve a transcript ... YouTube is blocking requests from your IP ... You are doing requests from an IP belonging to a cloud provider`.
- Watch pages fetched with curl returned HTTP 429. WebFetch of a watch page returned only the YouTube page chrome, with no description.

Three other routes were refused by the session's permission classifier as "Unauthorized Access" (working around YouTube's block). I did not retry them:

1. A direct call to YouTube's internal `youtubei/v1/next` and `/player` API.
2. Downloading an already-published third-party transcript of *Full Remotion Tutorial* (f393grXJn9E) at `https://sozai.app/transcript/full-remotion-tutorial-motion-graphics/`.
3. Downloading a third-party summary of the Vox video (7wuYBfE131U) at `https://videohighlight.com/v/7wuYBfE131U`.

To get transcripts, the user can either allow those third-party pages, or run yt-dlp from a residential IP or with their own cookies.

**What the notes are based on instead:**

- The channel's public RSS feed (`raw/rss.xml`), which gives full descriptions, chapters, exact publish dates and view counts for the 15 most recent uploads.
- The channel page listing (`raw/channel_flat.jsonl`, `raw/mo-sidd_videos.html`).
- The public Skool "about" page.
- The READMEs and agent docs of the tools he links, saved in `linked_readmes/`.

So the techniques below are **named by him in titles, descriptions and chapters**, with chapter timestamps. They are *not* step-by-step details from what he says in the videos. Where I add how to implement something, it is marked **[interpretation]**.

**How well he fits the goal.** MoSidd's channel is about **motion graphics built in code**: Remotion (React) plus Claude Code, for Vox-style explainers, documentary collages and viral Reels. It is *not* mainly about cutting talking-head footage. Only two videos are directly about editing real footage:

- **zCuthqXIAcg**: talking-head explainer with FilmCraft plus Remotion.
- **UW-jxCvuH9E**: automating a Premiere Pro edit with GPT-6.

His material is most useful for the **overlay, motion-graphics, B-roll, finish and audio-design layers** of a talking-head or ad edit. It is less useful for the cutting, de-filler and silence-removal layer. Section 6 lists other creators whose videos cover that layer directly.

---

## 1. Video index

Dates come from the RSS feed where available; otherwise the channel page's relative date (from 2026-11-13) is given. Durations come from yt-dlp's flat listing.

| # | Title | Date | Duration | Views | URL | Transcript? | Description / chapters? |
|---|---|---|---|---|---|---|---|
| 1 | I Made This Talking Head Explainer Using ONLY FilmCraft & Remotion (A/B title seen in search: "FilmCraft + Remotion Changed YouTube Editing Forever") | 2026-11-07 | 9:40 | 2.7K | https://www.youtube.com/watch?v=zCuthqXIAcg | No (blocked) | Yes, short |
| 2 | I Made This Viral Reel Using ONLY EffectCraft & Claude Code | 2026-10-25 | 5:45 | 45.9K | https://www.youtube.com/watch?v=DceFrd65KUg | No | Yes, detailed |
| 3 | I Automated My Entire Video Edit With GPT-6 (Premiere Pro) | 2026-10-17 | 9:38 | 2.8K | https://www.youtube.com/watch?v=UW-jxCvuH9E | No | Yes, short |
| 4 | I Made Documentary Motion Graphics Using Only Claude Code & Remotion | 2026-10-06 | 10:28 | 17.2K | https://www.youtube.com/watch?v=rK4vrMK4i2U | No | Yes, short |
| 5 | I Made This Minimal Reel Using ONLY Remotion & GPT 6 | 2026-09-21 | 13:57 | 11.2K | https://www.youtube.com/watch?v=GvC9zXk4l7s | No | Yes, plus chapters |
| 6 | Full Remotion Tutorial to Create Insane Motion Graphics | 2026-09-11 | 20:38 | 29.2K | https://www.youtube.com/watch?v=f393grXJn9E | No (third-party copy exists, see section 0) | Yes, plus chapters |
| 7 | I Made This SaaS Animation Using ONLY Claude Code & Remotion | 2026-08-06 | 13:49 | 24.3K | https://www.youtube.com/watch?v=b7KlsXNQobs | No | Yes, plus chapters |
| 8 | Create Viral Reels Using Only Claude Code & Remotion (Short) | 2026-07-27 | 0:33 | 6.5K | https://www.youtube.com/shorts/RWS7oSZFL2E | No | Teaser only |
| 9 | I Made This Viral Reel Using ONLY Remotion & Claude Code | 2026-07-26 | 13:30 | 153.8K | https://www.youtube.com/watch?v=xOhh274Ayac | No | Yes, plus chapters |
| 10 | Vox-Style Animated Charts With ONE PROMPT (Remotion + Claude Code) | 2026-07-18 | 5:21 | 5.0K | https://www.youtube.com/watch?v=dv3ADYu74DE | No | Yes, plus chapters |
| 11 | Claude Fable 5 + Remotion Built This $1,000 Collage Animation | 2026-07-11 | 7:10 | 20.6K | https://www.youtube.com/watch?v=aSNYHAzPEKc | No | Yes, plus chapters |
| 12 | I Built a Vox Explainer Using Claude Code & Remotion (No Plugins) | 2026-07-05 | 10:00 | 14.7K | https://www.youtube.com/watch?v=Y6mOBK5peDU | No | Yes, plus chapters |
| 13 | I Made Vox-Style Motion Graphics Using Only Claude Code & Remotion (**most viewed**) | 2026-06-28 | 13:11 | 269.2K | https://www.youtube.com/watch?v=7wuYBfE131U | No (third-party summary exists) | Yes, plus chapters |
| 14 | Claude Fable 5 vs Opus 4.8: Worth 2x the Price? (3 REAL Tests), which includes a Remotion test | 2026-06-15 | 8:07 | 468 | https://www.youtube.com/watch?v=W48cbXsIdzk | No | Yes, short |
| 15 | Codex vs. Claude Code: I Tested Both for 30 Days, which includes a Remotion animation test | 2026-06-02 | 12:16 | 466 | https://www.youtube.com/watch?v=fuqanqKQeMg | No | Yes, plus chapters |
| 16 | Create Animated Charts and Graphics Instantly with AI & Remotion | ~2026-02 ("9mo ago") | 18:28 | 5.9K | https://www.youtube.com/watch?v=dBakc0BdHjY | No | **No** (older than the RSS window) |

The other uploads are off-topic and were not covered: OpenClaw videos, Flux LoRA, dropshipping, finance and productivity Shorts from 2022. The full list is in `raw/channel_flat.jsonl` and `raw/channel_shorts_flat.jsonl`.

Coverage: 16 relevant videos indexed. 15 have full description text (`descriptions/*.txt`). 0 have transcripts.

---

## 2. Techniques, grouped by pipeline stage

Format: **technique**, then (video #, timestamp if a chapter gives one), then a note. An **[interpretation]** note is my suggestion for implementing it in a Claude Code skill. It is not from the video.

### 2.1 Philosophy and operating model

- **"No timeline, no keyframes"**: every element is code (Remotion/React) or a command in an agent-driven NLE, written by the agent from plain prompts (#9, #13, #6). "I didn't edit a single frame. Every animated cut-out, every chart that draws itself, every cut that lands right on the word, all of it is code that Claude Code wrote from plain prompts." (#13 description)
- **Few, large, spec-like prompts per piece.** Examples: 4 prompts for the collage (#11), 6 plain-English prompts for the map film (#12), 3 prompts for 3 charts or "ONE PROMPT" per chart (#10), "all four prompts" for the EffectCraft reel (#2), and one prompt plus an asset folder per 5-second vertical scene (#2).
- **"How to write prompts like specs so Claude Code builds exactly what you want"** (#6, inside the 14:24 build, per the description). **[interpretation]** Each prompt names the scene duration (frames and fps), canvas size, layer stack from back to front, the motion with easing for each layer, timing tied to voiceover words, and the finish effects. That matches how his descriptions break down each scene.
- **Every element stays editable by prompt.** You can tweak by hand in the tool's controls or change the same thing with a prompt (#2: "Tweaking manually in Effect Controls versus changing it with a prompt").
- **Cost awareness.** "$1,000-style collage animation with just 4 prompts and ~$4 in API credits" (#11). Chapter 1:55: "Every asset mapped + what it cost".
- **Model choice.** He ran Claude Fable 5 against Opus 4.8 on a Remotion motion-graphics test (#14) and Codex (GPT-5.5) against Claude Code (Opus 4.7/4.8) on a "Video Animation Test" (#15, 04:26-06:12). The verdicts are not available without transcripts. Later videos use **GPT-6 Astra** for storyboarding, building and sound effects (#3, #5), so he switches agents freely.

### 2.2 Pre-production: script, voiceover-first, storyboard, assets

- **Start from the voiceover and turn each VO line into a scene** (#5, 0:59 "Voiceover + storyboard": "How to start with the voiceover and turn each line into a scene"). The script/VO is the spine, and visuals hang off it.
- **Plan the script and visual style before any build** (#13, 1:30 "Planning the script and visual style").
- **The LLM storyboards the piece** (#5, 0:59 "How I storyboard a reel with GPT-6 Astra").
- **Decode a reference into a storyboard** (#11, 0:40-01:55 "Prompt 1: decode it + storyboard"). He gave the agent a reference piece, a collage showreel on Behance, and asked it to break the piece down into a storyboard. **[interpretation]** For ads: feed a reference ad (frames or a description) and ask for a shot-by-shot breakdown (duration, layers, motion, text, SFX cue) before building.
- **Build a tiny asset list and a 2-3 colour palette** (#5, 2:19: "Building a tiny asset list and a two-color palette"; "three base colors and very few assets"). Constraints are what make the minimal reel style work.
- **Map every asset and its cost** (#11, 1:55).
- **Use real, cited data for charts** (#10: "every chart runs on real cited data"; #4: "fetching market data to create clean, professional visuals"). The agent researches the numbers and keeps the sources.
- **Generate assets with AI image models.** Assets came from "GPT2 Image (Replicate)" (#11, 03:05 "Prompts 2 & 3: generate the pack, build the scene"). "All assets are AI-generated."

### 2.3 Project setup

- **Remotion install, two ways:** the terminal way, or let Claude Code set it up (#6, 3:06 "Installing Remotion + Studio tour").
- **Remotion Studio** is the review surface: "frames, the timeline, prop controls and rendering" (#6, 3:06).
- **Frame rate as a style choice:** "Setting up a 15 FPS Remotion project for that stop motion look" (#5, 2:19).
- **EffectCraft install and agent connection with one prompt:** "I install EffectCraft with one prompt, connect Claude to it" via "EffectCraft's MCP server" (#2). For the real setup commands, see section 3.
- **FilmCraft plus Remotion for real footage** (#1): "By connecting AI tools to your project, you can generate complex motion graphics without manual keyframing."

### 2.4 Talking-head and real-footage editing (the part most relevant to the skill)

Only two videos cover this. Neither transcript was obtainable.

- **#1 (zCuthqXIAcg), FilmCraft plus Remotion talking-head explainer.** From the description: "Enhance raw talking head footage using Filmcraft and ReMotion with AI. Build layered edits with motion graphics and voiceover. This workflow demonstrates how to **process audio** and automate visual production ... generate complex motion graphics without manual keyframing."
  - **[interpretation]** The split looks like this:
    - FilmCraft, driven by an agent over MCP, handles the NLE work: cuts, audio processing (its DSP has DeNoise, DeHummer, EQ, compressor, true-peak limiter and EBU R128 loudness meters), colour grade (Lumetri-style panel) and caption tracks.
    - Remotion renders the motion-graphics layers, which are composited over the talking head.
- **#3 (UW-jxCvuH9E), Premiere Pro automated with GPT-6 Astra.** "Cut your video editing time down from 8 hours to 30 minutes ... Editing usually involves tedious tasks like **cutting, audio cleanup, and assembling graphics** ... handling the heavy lifting, allowing you to focus on the narrative rather than the timeline." The description does not name the Premiere bridge (MCP or script).
- **Cuts land on the word** (#13: "every cut that lands right on the word"). Voiceover sync is a named stage (#9: "the voiceover sync and the final render"). **[interpretation]** You need word-level timestamps (Whisper or similar) and should snap scene and caption boundaries to word start times.

### 2.5 Motion graphics, overlays and B-roll-style inserts

- **Collage compositing, kinetic type and chart animation** as the core reel building blocks (#9, 1:07-11:47, "Building the collage animation scenes in Remotion"). This was a 6-scene documentary-style reel ("Netflix vs Blockbuster") over one voiceover.
- **Animated cut-outs and charts that draw themselves** (#13, 2:26 "Building the motion graphics scenes with Claude Code and Remotion").
- **Vox-style bar chart, with easing and a print-paper look** (#6, 6:50 Build 1; #10, 00:20 Chart 1 bar chart). Other chart types: **parliament chart** (#10, 02:20) and **"The One Clients Pay For"** (#10, 03:42).
- **The "one trick everyone gets wrong on hand-drawn animations"** (#10, description). The detail was not obtainable. **[interpretation]** It is likely stepping or boiling the hand-drawn line at a lower frame rate rather than animating it smoothly, which ties to "posterized time" below.
- **The "easing trick every animation needs"** (#12, 3:50). **[interpretation]** Never use linear interpolation. Use ease-in-out (cubic Bezier) or springs for every move: in Remotion, `interpolate(...,{easing: Easing.bezier(...)})` or `spring()`.
- **One continuous camera move** across the whole piece instead of hard cuts (#6, 11:12 Build 2 "Vox-style Mac timeline with one continuous camera move"; #12, 7:10 "One continuous shot + the film look"). **[interpretation]** Put all scenes on one large canvas under a single parent transform, and animate camera translate/scale along the VO timeline.
- **Transitions:**
  - "portal zoom" (#6, 14:24 Build 3)
  - "Pullback and push-in transitions" (#5, 11:56)
  - zoom-through-scene transitions in general
- **The sandwich trick plus posterized time** (#11, 05:00-06:15).
  - **[interpretation]** "Sandwich" probably means layering a subject cut-out between background and foreground copies, so elements can pass behind and in front of it. Use it for depth in collages and for text-behind-person on talking heads.
  - **[interpretation]** "Posterized time" means quantising animation time (for example holding each pose for 2-3 frames) for a stop-motion/collage feel. EffectCraft and FilmCraft both list a Posterize Time effect.
- **Keying trick** for jets and strikes on the map film (#12, 5:20). **[interpretation]** Key stock or AI-generated elements shot on flat backgrounds.
- **Maps without plugins:** world-atlas plus TopoJSON plus d3-geo for real country shapes and projections. "Prompt 1: the map engine" (#12, 1:00 and 1:40).
- **3D and glass:** glassmorphism, light and refraction, and 3D spheres with Three.js inside Remotion (#7, 1:56, 5:04, 9:42). This one is aimed at SaaS/product-demo marketing videos.
- **GSAP** listed as part of the stack for the minimal reel (#5).
- **Scene examples from the minimal reel** (#5): "a 3D eyeball scanning social media, with a vision cone and halftone finish" (4:26), "a swinging, flickering light and a battery filling from 0 to 100%" (8:04), and "a bobbing iceberg, waves, a buoy and a moonlit sky" (10:01).

### 2.6 Finish, look and "colour" (stylisation layers rather than a classic grade)

He builds the look as a **shared finish stack applied over every scene**: "a shared print finish" (#5, 11:56) and "the film look" (#12, 7:10).

- **Print paper look:** a set of layers he breaks down in #10 ("break down the layers that make the 'printed paper' look"), also covered in #6 Build 1.
- **Halftone magazine finish** (#6 Build 2; #5 Scene 1).
- **Film grain plus TV scanlines** (#6 Build 3; #12 film grain).
- **EffectCraft finishing stack for a vertical reel scene** (#2), in this order: "window light, grain, grunge, Venetian Blinds scan lines, tint reveal, vignette".
- **[interpretation]** For talking-head ads, the matching tools are a subtle grain, a vignette and a brand-tint LUT applied consistently across all segments, plus a consistent overlay palette (the 2-3 colour rule).

### 2.7 Audio: voiceover, music, foley and SFX

- **Voiceover:** ElevenLabs (#5, #12). "Voiceover done with AI" for the viral reel (#6 links #9).
- **Music:** Google **Lyria 2** (#11) and **Magnific** (#12).
- **SFX and foley:** ElevenLabs sound effects (#12, 8:10 "A narrator, a score and the foley"), GPT-6 Astra for sound effects (#5), and "Prompt 4: music + foley" (#11, 06:15). Sound design is a named final pass (#5, 11:56 "Transitions, finish + sound").
- **Audio cleanup and processing** on real footage (#3; #1 "process audio"). The tools were not named. FilmCraft has DeNoise, DeHummer, EQ, dynamics, a limiter and EBU R128 metering.
- Overall order: build the visuals, then add narrator, score and foley as the last stage (#13, 11:01 "Voiceover, music and final render"; #12, 8:10). The VO *script* comes first, though, as the timing spine (#5).

### 2.8 Render, export and review loop

- **Review in Remotion Studio and tune by prompt** (#12, 4:30 "Tuning Scene 1 in Remotion Studio"; #13, 8:00 "Assembling and fine-tuning the edit"). The loop is: build a scene, preview it in Studio, ask for adjustments, repeat. Then assemble the scenes and do the final render.
- **Vertical export:** "Exporting a 1080 x 1920 MP4 with audio, by hand or by prompt" (#2).
- **Build scene by scene, then assemble.** Every multi-scene video is structured as per-scene builds (#5, #9, #12) followed by transitions, finish, sound and render.

### 2.9 Short-form vertical (Reels/Shorts) and ads

- **Format:** 1080x1920 MP4 with audio (#2). Scenes are about 5 seconds each (#2: "a complete 5-second vertical scene from a single prompt and an asset folder").
- **Viral reel structures he uses:**
  - documentary collage with one VO and 6 scenes (#9)
  - minimal 3-colour stop-motion at 15 fps with 3 scenes (#5)
  - EffectCraft scene with a heavy finish stack (#2)
- **His hook claim:** "Reels like these have been going viral and editors charge hundreds of dollars for them" (#5). The positioning is "the same workflow behind the viral reels you see getting millions of views on Instagram and TikTok" (#9).
- **Ads and marketing:** the SaaS glass/3D animation is pitched for "marketing or product demos" and "founders who need launch videos without an agency" (#7; Skool about page).
- **No specific talking-head ad rules** (hook timing, caption styles, safe zones, CTA cards) could be extracted without transcripts.

---

## 3. Linked repos and tools (with URLs)

| Tool | URL | What it is / how he uses it | Install / connect (from official docs, not run here) |
|---|---|---|---|
| **Remotion** | https://www.remotion.dev | Makes videos from React components. His core engine for every motion-graphics build. Remotion Studio is the preview and tuning UI. | Remotion Claude Code plugin: `claude plugin marketplace add remotion-dev/claude-code-plugin`, then `claude plugin install remotion@remotion`, then restart Claude Code. Slash command: `/remotion:remotion-create <prompt>`. |
| **Remotion Agent Skills** | https://github.com/remotion-dev/remotion/tree/main/packages/skills (docs: https://www.remotion.dev/docs/ai/skills) | Official SKILL.md rules for agents. Skill areas: `remotion-markup` (compositions, animation, layout, typography, media, effects, audio, fonts, timing), `remotion-captions`, `remotion-maps`, `remotion-multimedia` (Mediabunny metadata), `remotion-interactivity` (Studio-editable props). `/remotion-best-practices` is the umbrella skill. He does not explicitly name these skills; #12 is titled "No Plugins". | `npx remotion skills add`, or `npx skills add remotion-dev/skills`, or `gh skill install remotion-dev/skills`, or `npx create-video@latest --skills` |
| **Remotion Claude Code plugin** | https://github.com/remotion-dev/claude-code-plugin | Plugin that bundles the skills above. | See above |
| **Claude Code** | https://claude.com/claude-code | The agent that writes the Remotion code. He used Claude Fable 5 for the collage (#11) and compared it with Opus 4.8 (#14). | |
| **GPT-6 Astra** (OpenAI) | n/a | Alternative agent he used for storyboarding, building, SFX (#5) and the Premiere Pro automation (#3). Also connected to EffectCraft via MCP (#2). | |
| **FilmCraft** (ArtCraft team, storytold) | https://github.com/storytold/filmcraft and https://getartcraft.com/apps/filmcraft | Open-source Rust NLE in the style of Premiere (alpha; the README rates it about 56% "ready for real work"). Over 650 engine commands are exposed via CLI, a JSON control channel and an **MCP server**, so an agent can cut, trim, grade, mix, caption and export. He used it for real talking-head footage (#1). Relevant features: Lumetri-style colour, audio DSP (DeNoise, DeHummer, EQ, limiter), EBU R128 meters, SRT/VTT caption tracks with burn-in, H.264 export, and FCP7 XML / FCPXML / OTIO / EDL / AAF interchange. Speech-to-text is optional and off by default. | `claude mcp add filmcraft -- filmcraft-cli mcp` (CLI ships with the deb/rpm; separate zip on macOS). Headless: `filmcraft-cli mcp --project p.fcproj`. Bridge to the running app: `filmcraft --control 9876` plus `filmcraft-cli mcp --bridge 127.0.0.1:9876` with `FILMCRAFT_CONTROL_TOKEN` set. Agent loop from its docs: `project_inspect`/`sequence_inspect`, then `command_run`, then `render_frame`/`ui_screenshot`, then `edit.undo` if wrong. Notes in `linked_readmes/filmcraft_docs_agents.md`. |
| **EffectCraft** (ArtCraft team) | https://github.com/storytold/effectcraft and https://getartcraft.com/apps/effectcraft | Open-source Rust motion-graphics/VFX app in the style of After Effects: 259 effects, 3D layers, expressions, Lottie, `.ecproj` JSON projects, MCP server. He used it for a vertical reel scene (#2). | `claude mcp add effectcraft -- effectcraft-cli mcp` (headless) or `effectcraft-cli mcp --bridge 9877` with the app started as `effectcraft --control 9877`. Render: `effectcraft-cli render main.ecproj --comp Main --out main.mp4`. Contact-sheet check: the `render_frame` tool with `times:[...]`. Docs: https://craft.wiki/apps/effectcraft/overview/ |
| **Craft Launcher** | https://github.com/storytold/craft-launcher | Installer and updater for the Crafting Apps. | |
| **GSAP** | https://gsap.com | JS animation library used in the minimal reel (#5). | |
| **Three.js** | https://threejs.org | 3D spheres and refraction inside Remotion (#7). | |
| **world-atlas + TopoJSON + d3-geo** | https://github.com/topojson/world-atlas, https://github.com/topojson/topojson, https://github.com/d3/d3-geo | Free country shapes and map projections for map animations (#12). | |
| **ElevenLabs** | https://elevenlabs.io | Voiceover and sound effects (#5, #12). | |
| **Lyria 2** (Google) | n/a | AI music (#11). | |
| **Magnific** | https://magnific.ai | Music for the map film (#12), per his description. | |
| **GPT Image via Replicate** ("GPT2 Image") | https://replicate.com | AI-generated collage assets (#11). | |
| **Skool: AI Visual Production Lab** | https://www.skool.com/ai-visual-production-lab-4976 | His free community (about 7.7K members). The about page says it holds "Full project files from every video: skill files, storyboards, scripts, assets" and "Plain-steps build guides". **His actual prompts and skill files are behind a Skool login, which I did not use.** | Requires sign-in |
| Survey | https://tally.so/r/RGXj5Q | Lead-gen survey offering a free 20-minute call. Not relevant. | |

---

## 4. Prompts he shows (direct quotes)

**None could be quoted.** He shows the prompts on screen in the videos, and the transcripts are blocked. He also distributes them only inside the Skool community: "All four prompts, the project file and every asset are free in my Skool community" (#2), and "All the prompts and asset files are free in my Skool community" (#7, #9).

Prompt structure as described in his descriptions (paraphrased; not verbatim prompts):

- #11, 4 prompts:
  1. decode the reference and storyboard it
  2. generate the asset pack
  3. build the scene
  4. music and foley
- #12, 6 prompts. Prompt 1 is "the map engine". The rest are per scene, then the film look, then narrator, score and foley.
- #10: one prompt per chart (3 charts).
- #2: 4 prompts. One installs EffectCraft and connects Claude or GPT. One builds a full 5-second vertical scene "from a single prompt and an asset folder". Then finishing effects, then export to 1080x1920 "by prompt".
- #6: "How to write prompts like specs so Claude Code builds exactly what you want."

Example prompt from Remotion's own docs (not his): `/remotion:remotion-create Make a promo video for a record store`.

---

## 5. Quality rules and mistakes he warns about (from titles and chapters only)

- Always use easing; "the easing trick every animation needs" (#12, 3:50).
- Hand-drawn animations: "the one trick everyone gets wrong" (#10). The detail was not obtained.
- Prefer one continuous camera move to disjointed cuts in explainers (#6, #12).
- Keep the palette to 2-3 colours and the asset list tiny for minimal reels (#5).
- Apply one shared finish (grain, halftone or print) across all scenes so the piece reads as a single film (#5, #12).
- Make cuts and graphics land exactly on the spoken word (#13).
- Charts must use real, cited data (#10).
- Check every scene in Remotion Studio before assembly, and tune with follow-up prompts (#12, #13).

---

## 6. Gaps, and better sources for the talking-head cutting layer

These come from the same YouTube searches (`raw/search_*.html`). None were researched further. Each one's title says it covers Claude Code editing of real talking-head or Reels footage, so they are candidates for transcript research if access becomes available:

- Christian Peverelli: "I Fully Automated My Video Editing Using Claude Code (Full Walkthrough)", https://www.youtube.com/watch?v=HzXD4GVqXwM (923K views)
- Matt Loui: "Automate Your CapCut Editing With Claude (Step by Step + Free Skill)", https://www.youtube.com/watch?v=U-AdnIz1jIk (299K)
- Jason Cooperson: "How I Fully Automated My Video Editing (Claude Code)", https://www.youtube.com/watch?v=XeTAlZiIWHE (260K)
- kaye.creatives: "Claude Edited My Entire Reels Video in 35 Minutes", https://www.youtube.com/watch?v=FJZkfjM8WhI (217K)
- Rourke: "How to Edit Instagram Videos With AI (Claude Code)", https://www.youtube.com/watch?v=M59zhPRXg1I (125K)
- Eddie: "Claude Code Can Now Clip ANY Video (Free Skill)", https://www.youtube.com/watch?v=IY08-3TS2o8 (119K)
- Matt Wolfe: "How I Get Claude To Edit My Videos (Step-By-Step)", https://www.youtube.com/watch?v=ep4psgAFOqc (103K)
- Lucas Leite: "How to edit videos with Claude Code in practice (full tutorial)", https://www.youtube.com/watch?v=zB0_5-e5V1Y
- Brian Casel: "Watch Claude Code edit my YouTube video", https://www.youtube.com/watch?v=GlvH_waCx8w

---

## 7. Files in this folder

- `NOTES.md`: this file.
- `descriptions/<date>_<videoId>.txt`: full description text for each video (the stand-in for transcripts).
- `raw/rss.xml`: channel RSS feed (source of descriptions and dates).
- `raw/channel_flat.jsonl`, `raw/channel_shorts_flat.jsonl`: yt-dlp flat listings (titles, durations, views).
- `raw/mo-sidd_videos.html`, `raw/channel_videos.html`: the `@mo-sidd` channel page and the empty `@mosidd` page.
- `raw/search_*.html`: YouTube search result pages used to find the channel.
- `raw/ytdlp_retry_error.txt`: the exact yt-dlp error.
- `linked_readmes/`: READMEs and agent docs for FilmCraft, EffectCraft, ArtCraft and Craft Launcher (read only, nothing run).
- `scripts/`: the small parsers used here.
- `.venv/`: isolated venv with yt-dlp and youtube-transcript-api.

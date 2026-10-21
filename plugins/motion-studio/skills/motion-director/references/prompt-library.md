# Prompt library

Prompts that produced the strongest results in the 2026 coded-motion wave, with their sources, followed by Adsworm templates for premium Meta ads. Treat each one as a starting brief. Swap in real assets and approved claims.

## Proven public prompts

**SaaS launch film (Remotion).** Axel Schapmann. Source: https://youmind.com/video-prompts/saas-launch-video-remotion-11509
> Act as a senior motion designer and build a 30-second launch video for [product] in Remotion, entirely in code so I can edit and re-render it: first read my landing page and codebase to pull the real story, copy, colors, font and logo file (trace the logo to SVG so it stays sharp and can be animated), then write the video as one story (why the market matters, why it's painful today, how [product] fixes it, what you get) in 4 to 5 scenes with one short title each, animate everything like a premium product film (kinetic typography word by word, spring easing, smooth camera pushes and pans, depth and glow, elements that build in on the beat instead of just appearing), keep each scene on screen long enough to read, add one soft sound effect for every element that appears and silence otherwise, and end on a memorable animated logo reveal with the tagline and URL, then render it, check the frames yourself and fix anything that overlaps, clips or feels rushed before showing me the result.

**Showreel → product film.** Ihab Khattab, via https://www.ayautomate.com/resources/claude-opus-5-5-motion-graphics
> Make a dynamic 30-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. Go all out. Introduce the product, use actual product screenshot/logo/assets. Must have music and motion must match the music. Do it like a real professional production video, not a demo or prototype. Add more animation and motion design; avoid using screenshots as raw, instead break them down into components/icons so they can be animated too. Make the motions juicier. Use the best motion design techniques you can.

**Apple-keynote discipline.** zero (@twoclipping), excerpt, same source. Steal the bans and the beat map:
> Banned: crossfades, blur-ins, 3D flips, particles, glows, holds longer than 1 second, anything that looks like a template. Structure: build to 120 BPM, 54 beats, something happens on every beat. … Ask for the inputs, then show a beat map and 4 still frames … before rendering the full film.

**Launch from a URL (HyperFrames).** Source: https://hyperframes.heygen.com/guides/prompting
> /product-launch-video Make a 45-second 1920x1080 launch video for https://linear.app . Energetic but minimal, use the site's own palette and screenshots. Structure: hook stating the problem, 3 feature beats with UI captures and one-line captions, end card with logo + "Try it free". Female TTS voice, confident tone, subtle electronic BGM under -18dB.

**Single kinetic stat (HyperFrames).** Same source, excerpt:
> /motion-graphics 6-second 1920x1080 video, dark navy background. Beat 1 (0-1s): label "ARR" fades up small, top-center. Beat 2 (1-4s): a giant number counts up to $4.2M with an odometer roll, easing out as it lands. Beat 3 (4-6s): "+312% YoY" stamps in below in green, then everything settles into a gentle ambient idle.

**Apple-style promo from a site.** @wiedymi, via https://www.remotion.dev/prompts
> Make a promotion video in Apple presentation style for VVTerm. Check its website VVTerm.com for details and assets like logo. Use nerd fonts and inter. Make it around 20 seconds.

**Kinetic charts.** Charlie Hills's method:
1. Pick one motion, such as a chart that morphs.
2. Show a reference and name every state.
3. Ask for HTML/SVG and fix it round by round.

## Adsworm templates (premium Meta ads)

Each one assumes `brands/<client>/brand.json` exists and the `remotion-ad-kit` template is scaffolded.

**Luxury DTC: product hero (10–12 s, 9:16 + 4:5)**
> Using the remotion-ad-kit and brands/<client>/brand.json, build a 12-second ad for <product>. Motion personality: luxury (slow outExpo entrances, one element per beat, generous negative space, serif-italic accents). Scenes: hook (problem in ≤6 words), product hero with the real cut-out PNG, one proof point from the approved claims list, offer + CTA end card. No particles, no glows, no bounce. Show the storyboard with frame ranges and 4 stills before rendering. Then run npm run qa, read the sheets, and fix the 3 worst defects.

**Performance DTC: offer stack (8–10 s)**
> Same kit, motion personality: performance (snappy springs, 12–18 frame entrances, push-cut transitions). Hook names the pain in the first 0.5 s. Stack three benefit chips, then a price anchor (strike-through RRP → offer price), then urgency and CTA. Keep every word inside the Reels safe zone. Render 9:16 and 4:5, then run meta-delivery-qa.

**Hybrid: AI footage + coded type**
> Generate a 5-second <scene> clip with <Higgsfield/fal/Runway>, 1080×1920, no text in frame. Put it in public/ and set backgroundVideo. Keep the kit's scrim. The kinetic hook and end card stay coded so copy stays sharp and editable across variants.

**Variant sprint**
> Write props/matrix.json with 3 hooks × 2 offers × 1 CTA for <campaign>, formats 9:16 and 4:5. Dry-run first and tell me the render count, then render, then hand me manifest.csv with the Meta ad names.

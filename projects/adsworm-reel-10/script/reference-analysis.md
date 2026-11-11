# Reference module dissection (owner-supplied reel, 21 Oct 2026)

Reel: instagram.com/reel/DevHJjxvSFJ by @ganesh.debnath__ (Meta-ads educator). 74.8 s, 1080×1920, 30 fps. 215 likes / 74 comments within a day. Pulled via yt-dlp; frames and audio analysed locally; transcribed with faster-whisper (small).

## What the module is
**Two 2D cartoon avatars having a Hinglish conversation under a "receipts" card.**

| Layer | What it does |
|---|---|
| Top card (y≈120–980) | White rounded "whiteboard". Section label top-left (① FIRST IMPRESSION ADS), status tag top-right (official · test). Content builds element by element as the voice mentions it: official page with URL bar + date, phone mockups, a 24 h ring, a Meta research chart, an IG comment UI for the CTA. Tiny source line at the bottom ("Source: Meta for Business · Brand Building Summit, 15 Oct 2026"). |
| Caption bubble (y≈1040–1200) | One short Hinglish sentence (Latin script) per ~2.5 s, 1–2 keywords in blue pills, speaker tag (GANESH / FOUNDER) that alternates → a dialogue, not a monologue. |
| Avatars (y≈1220–1760) | Creator cartoon (likeness) on the right, "Founder" on the left, standing on a blue platform; poses swap (point, thumbs up, wave, think) with each line. |
| Footer | "Ganesh Debnath \| Full Stack Performance Marketer" on the platform, always visible. |

## Measured mechanics
- **Zero hard cuts** (ffmpeg scene detection at 0.3 found none). Change comes from the card building and captions swapping, not from editing.
- **Voice-led.** Speech-band energy is 46% of the mix; only 4 pauses ≥ 0.4 s in 75 s. No steady musical beat (bass autocorrelation 0.16). A light bed at most.
- **Pace:** ~30 caption lines in 75 s ≈ 2.5 s/line, ≈ 3.5 words/s.
- **Script architecture:** identity call-out ("Founderji!") → credibility ("6 saal se") → novelty ("aisa update kabhi nahi dekha") → emotion ("dimaag ghoom gaya 🤯") → promise/open loop ("Teen bade updates") → ①②③ each with receipt + a Founder reaction ("Sabse pehla ad? Wah!", "Matlab Diwali sale ki raat sirf mera brand") → bonus insight with a chart → "Comment UPDATE" → free PDF + official link in DM → "Save karo".
- **Light theme.** Off-white/pale-blue background, white cards, one blue. It reads as *content*, not as an ad.

## Why our two earlier reels failed against this
1. Dark cinematic kinetic type reads as an ad; no voice → nothing to follow with the ears, so the eye has to read everything.
2. Abstract metaphors instead of receipts → nothing concrete to believe.
3. Monologue; no second voice to react, so no conversational pull.
4. Sound cues fired at the first frame of each animation while the visual landed 3–6 frames later (audio led video) → "not synced". Here, captions and card builds are driven by the TTS word timings, so sync holds by construction.

## What we keep from the brand
Same blue (#1B5EF7 ≈ the reference's blue), navy ink, gold for proof, Bebas Neue for card numbers, DM Sans for captions, cream paper instead of pale blue.

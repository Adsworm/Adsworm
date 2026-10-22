# Adsworm Reel Playbook: hooks, dialogue, voice, motion

For 40–50 s AMAN/RIYA explainers. Researched 22 Oct 2026. Sources are listed at the end.

## 0. Why reel A failed
- **It answered before it asked.** "Price per ad rose twelve percent" is a fact, not a curiosity gap. Reel B opened with a threat to *my* ads plus a date.
- **Five numbers and two inline definitions** ("CPM, the price of…"). It played as a lecture.
- **Riya was a polite interviewer** ("What do I actually fix?"). She never made a mistake, laughed or pushed back.
- **No analogy**, so the paradox (ads cost more, sales got cheaper) never clicked. **No callback ending** either.

## 1. Hooks: the first 3 s
Mosseri (head of Instagram): the first 3 s are "the hook", and it needn't be bait. Jenny Hoyos: the hook is 3 s or less, there's no preamble, and **the conflict is in sentence one**. Write at a 5th-grade reading level.

| Formula | Examples | Visual, 0–3 s |
|---|---|---|
| Curiosity gap / paradox | "Ad prices are about to shoot up… and smart brands are HAPPY." · "Ads cost more. Sales got cheaper. How?" | The two clashing words slam in on opposite sides, then a "?" pops |
| Pattern interrupt | Riya: "STOP. Don't touch that budget!" · Aman drops his phone mid-word | A hard zoom-punch on a character already in motion |
| Contrarian | "Pausing ads before Diwali is your most expensive mistake." · "Cheap ads are a trap." | A red ✗ stamps over the belief |
| You're doing X wrong | "Cutting ad spend this month? Watch this first." · "You're judging ads by the wrong number." | The wrong thing appears, then gets struck through |
| Relatable pain | Riya: "Same budget. Half the sales. WHY?" · "Ads feel expensive? You're not imagining it." | Riya's reaction plus the pain phrase as text (most viewers watch muted) |
| Story-open | "A client almost paused everything last November…" · "Riya was one click from switching ads off." | A cold open with the action already happening |

Rules:
- Make it clear who the reel is for. Clarity beats clever.
- Voice, text and visual carry the **same** idea.
- Always pay the hook off.

## 2. Retention structure (40–45 s)
- **One idea per reel.** A second payoff makes the retention curve sag.
- **Open the loop at 0 s** and pay it off around 60–70% of the way in (~28 s). Then give the action and the CTA.
- **Re-hook every 5–8 s:** a new card state, a sound, a question or a speaker change.
- **Micro-loops:** every answer opens the next question ("Then how…?").
- **Silence:** about 0.5 s, and only right before the payoff. Never let the reel *sound* like it's ending.
- **Loop the ending:** Riya's last line echoes the hook's words. That drives rewatches and sends, which Mosseri ranks highly.

## 3. Dialogue psychology
**The evidence.** In Derek Muller's PhD studies (Veritasium), videos where a student *voices the misconception* and a teacher corrects it roughly **doubled** test scores versus clear lecture videos. So **Riya must say the wrong thing out loud.**

**Do:**
- **Tension:** Riya proposes the wrong move ("I'm pausing everything!") and Aman *interrupts*.
- **The dumb question:** Riya says "Wait, how?" so the viewer doesn't have to.
- **One everyday analogy** (a shop, a mela, a taxi surge) instead of any definition.
- **A laugh beat** in the first 10 s: disbelief, sarcasm, or something cheeky.
- **Short turns:** no one gets more than 2 lines in a row, and each line is 12 words or fewer.
- **The click:** Riya restates the idea in her own words.
- **Arc:** panic → confusion → relief → smug.

**Kills it:**
- Stats back to back, or more than 2 spoken numbers.
- Jargon (CPM, ROAS) or inline definitions.
- Polite Q&A.
- Filler ("Partly. Here's what's happening…").
- Spoken sources. Put them on the card.

**Turn-by-turn template:**

| Turns | Time | Who | Beat |
|---|---|---|---|
| 1 | 0–3 s | A or R | Hook: paradox or pain |
| 2 | 3–5 s | R | Laugh or disbelief |
| 3 | 5–9 s | A | Stakes: number #1 (receipt on the card) |
| 4 | 9–12 s | R | The wrong move (tension) |
| 5 | 12–16 s | A | Interrupts: "Don't!" + number #2 |
| 6 | 16–18 s | R | "Wait, how?" |
| 7–8 | 18–25 s | A | Analogy, slower |
| 9 | 25–28 s | R | Restates it: the aha |
| 10–11 | 28–35 s | A | One action, 3-word items |
| 12 | 35–38 s | R | A personal doubt |
| 13 | 38–42 s | A | CTA keyword |
| 14 | 42–45 s | R | Callback to the hook |

## 4. Tonality and voice
- **Energy curve:** hook 9 → stakes 6 → tension 8 → analogy 5 (slower, warmer) → aha 7 → CTA 8. Flat energy is what sounds "manufactured".
- **Pace:** about 165–175 wpm. Rush the stakes, slow the analogy.
- **Emphasis:** one CAPS word per line at most, since ElevenLabs stresses CAPS. Use "…" for a beat before the payoff and "-" for an interruption.

**Audio tags: officially supported.** ElevenLabs documents inline `[tags]` for **Eleven v3 and v4** (v4 launched 28 Sep 2026). That includes the **Text to Dialogue** endpoint we use: one call, `inputs[]` of text + voice_id, at most 2,000 characters.
- Emotions: `[excited] [curious] [sarcastic] [worried]`
- Delivery: `[whispers] [shouts] [rushed] [slowly] [pause]`
- Reactions: `[laughs] [chuckles] [sighs] [gasps]`
- Dialogue: `[jumping in] [interrupting] [overlapping]`

How to use them:
- v4 lets you stack tags, and the tag list is open-ended.
- Put one tag (two at most) at the **start** of a line.
- Match tags to the voice. A calm voice given `[shouts]` may read the tag aloud.
- Render 2–3 takes with a fixed `seed`.

Our pipeline:
1. Higgsfield's `elevenlabs_v4` passthrough of tags isn't documented. Run a 2-line test (~1 credit) first.
2. Add a `tags` field and send `tags + say` to TTS. Keep `say` clean, because `voice.py` aligns Whisper output to it.
3. Exempt `[laughs]`/`[pause]` lines from `gapCap`, or the trim cuts them.

**Free alternatives:** neither beats v4 at ~5 credits a reel, so stay on v4.
- Dia (Apache-2.0) does `[S1]/[S2]` dialogue with `(laughs)`, but it's slow, English-only and has no Indian voice.
- Chatterbox (MIT) has emotion control but no dialogue mode.

## 5. Hook motion (Remotion, free packages)
Frame 0 must already be a readable, finished composition. No fade-in.
1. **Zoom-punch (frames 0–8):** scale 1.25→1 with `spring({damping:12, stiffness:200})`. Add `<CameraMotionBlur>` (`@remotion/motion-blur`), a 2-frame white flash at 25%, and a "thump" SFX.
2. **Kinetic type on word timings:** each key word drops in on its spoken frame (y 40→0 on a spring). The CAPS word bumps 1→1.15→1 and turns gold. Other words sit at 60% opacity. Captions show 3–5 words at a time via `createTikTokStyleCaptions`.
3. **Object morph:** `evolvePath` draws a rising price line. On the key word, `interpolatePath` (`@remotion/paths`) morphs it into a new shape over about 10 frames.
4. **Number land:** count up with `interpolate` + `Easing.out(Easing.cubic)` over 15 frames, using tabular digits. Then a 6-frame shake (`@remotion/noise`) and a "pop".
5. **Match-cut:** the hero object stays in the same spot across the cut. Use slide or wipe with `springTiming({config:{damping:200}, durationInFrames:12})` (`@remotion/transitions`).
6. **Never static:** a 1.00→1.04 push-in on every card, a 4-frame squash pop on the speaker, and a nod from the listener.
7. **Starter code:** `reactvideoeditor/remotion-templates` (Popping Scale Text, Stat Counter, Text Highlight).

## 6. Who to copy
1. **Griffin Drops Knowledge** (AI Peter & Stewie explainers): the clueless character's wrong move drives every video. *Copy:* Riya proposes the mistake first.
2. **Two Cents** (PBS, an animated finance show with two hosts): they disagree, then settle it with a daily-life example. *Copy:* real friction before the answer.
3. **Sharan Hegde** (3M+ followers, comedic finance skits): relatable Indian analogies. *Copy:* exactly one everyday analogy per reel.
4. **INDmoney's two-character films:** one character wins and the other lets their money sleep. *Copy:* show the two choices as characters, not as bullets.
5. **Jenny Hoyos** (Shorts strategist): conflict in sentence one. *Copy:* check every script in Hemingway Editor and keep it at grade 5 or lower.

## 7. Reel A rewritten: "Prices UP, sales CHEAPER"
The script is 114 words and runs about 42 s. It speaks 2 numbers (59 and 20). The 12% and 48% figures appear only on cards.

| # | Who | Tags | Line |
|---|---|---|---|
| 1 | AMAN | `[excited]` | Ad prices are about to shoot up… and smart brands are HAPPY. |
| 2 | RIYA | `[laughs] [sarcastic]` | Happy? Are they okay? |
| 3 | AMAN | `[chuckles]` | Last Black Friday week, ad prices ran fifty-nine percent above September. |
| 4 | RIYA | `[panicking]` | That's it. I'm pausing everything till December- |
| 5 | AMAN | `[jumping in]` | Don't! Same week, each sale cost twenty percent LESS. |
| 6 | RIYA | `[confused]` | Wait… ads cost more, but sales got cheaper? How? |
| 7 | AMAN | `[warmly] [slowly]` | Think of a shop on a festival weekend. |
| 8 | AMAN | `[warmly]` | Rent's higher… but people walk in ready to BUY. |
| 9 | RIYA | `[gasps] [excited]` | Ohhh! Expensive crowd, but a buying crowd! |
| 10 | AMAN | `[confident]` | Exactly. So don't vanish. Fix what happens after the click. |
| 11 | AMAN | `[rushed]` | Clear offer. Fast page. Easy checkout. |
| 12 | RIYA | `[worried]` | Umm… and if my page is slow? |
| 13 | AMAN | `[excited]` | Comment OCTOBER. We'll find where your money leaks, free. |
| 14 | RIYA | `[whispers] [cheeky]` | Doing it before prices shoot up. |

**Cards (not spoken):**
- Line 1: "+12% avg price per ad · Meta Q2 2026".
- Lines 3 and 5: "CPM +59% · cost per sale −20% · Lebesgue · median brand · BF week 2025 vs Sep · not India data".
- Line 8: "+48% conversion rate".

**Hook visual:** on frame 0, a price tag zoom-punches in while its line graph shoots up. On "HAPPY" the arrow morphs into a smile, and a gold "HAPPY?" stamps in beside Riya's laughing face.

## Sources
- https://news.inman.com/2025/03/07/head-of-instagram-reveals-secrets-to-social-media-success/
- https://www.opus.pro/blog/instagram-reels-hook-formulas
- https://faceless.so/blog/25-hook-formulas-for-short-videos-that-keep-viewers
- https://jellymarketing.ca/blog/stop-the-scroll-in-3-seconds-secrets-to-high-performing-short-form-video-hooks/
- https://tlinky.com/3-second-hook/
- https://www.capcut.com/create/short-form-video-hooks
- https://marketing-examined.beehiiv.com/p/jenny-hoyos-shortform-video-playbook
- https://www.demandcurve.com/newsletters/growth-newsletter-187
- https://www.gofaceless.ai/blog/optimize-video-engagement-pattern-breaks
- https://skills.sh/iart-ai/tiktok-video-skills/short-form-video
- https://www.socialync.io/blog/retention-techniques-keep-viewers-watching-2026
- https://thejournal.com/articles/2015/05/05/watching-videos-does-not-necessarily-lead-to-learning.aspx
- https://elevenlabs.io/docs/capabilities/text-to-dialogue
- https://elevenlabs.io/blog/v3-audiotags
- https://help.elevenlabs.io/hc/en-us/articles/35869142561297-How-do-audio-tags-work-with-Eleven-v3
- https://elevenlabs.io/docs/best-practices/prompting/eleven-v3
- https://techcrunch.com/2026/09/28/elevenlabs-new-v4-speech-model-supports-more-expression-control-and-90-languages/
- https://github.com/nari-labs/dia
- https://tts.ai/blog/open-source-text-to-speech-guide-2026/
- https://www.remotion.dev/docs/transitions
- https://www.remotion.dev/docs/motion-blur
- https://www.remotion.dev/docs/paths/interpolate-path
- https://www.remotion.dev/docs/captions/create-tiktok-style-captions
- https://github.com/reactvideoeditor/remotion-templates
- https://www.snapchat.com/@griffindropsai
- https://www.pbs.org/show/two-cents/
- https://www.khaleejtimes.com/business/markets/dubai-indian-social-media-finance-guru-gains-millions-of-followers-with-no-technical-degree
- https://www.exchange4media.com/advertising-news/indmoneys-latest-campaign-urges-indians-to-take-charge-of-their-finances-138476.html

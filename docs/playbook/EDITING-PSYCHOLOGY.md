# Editing Psychology Rulebook for AMAN/RIYA reels

Researched 11 Nov 2026. Companion to `REEL-PLAYBOOK.md`.

Labels: **[S]** study or platform statement, **[W]** weak (working paper, survey, secondhand), **[F]** creator folklore, **[I]** our inference. Most studies used lectures, radio, text or banner ads, not Reels, so test every number.

## 1. What Instagram says it ranks on
- **Top signals** [S]: "The top three signals that matter most for ranking are watch time, likes and sends." Sends weigh more with non-followers (Mosseri, Jan 2025) [1].
- **Less visible** [S]: low-res, watermarked, muted, mostly-text or reposted reels (Mosseri, 31 May 2023) [2].
- **Skip rate** [S]: "percentage of views where viewers skip a Reel within the first 3 seconds" (Meta, 3 Dec 2025) [4]. Retention chart: "the flatter the line, the more engaged" (Aug 2025) [3].
- **Originality** [S]: "clickbait or engagement bait" may be ineligible for recommendations (30 Apr 2024) [5]. Mosseri's 31 Dec 2025 memo: "Continue to improve ranking for originality", "Label AI-generated content" [7].
- **Length** [S]: "We won't recommend Reels that are over 90 seconds long" (June 2024) [6].
- **Folklore, not Instagram**: "saves matter most", "sends count 3–5× likes".

KPIs: skip rate, retention slope, sends per reach.

## 2. Attention and retention
- **Cadence** [W]: 50 top talking-head TikToks had a median of 0.33 cuts/s (16th–84th percentile 0.19–0.52). In a 242-person experiment, high pace *reduced* intent to finish or rewatch [8]. Each cut triggers an orienting response; too many drain capacity for the message [9] [S, theory].
  - **Rule:** one board-level change every 2–4 s, never over 2 per second. Counts: new element, state flip, sticker, speaker swap, reaction, punch-in, whip. Not: karaoke highlight, mouth flap, dot drift.
- **Punch-ins** [F]: scale 1.00→1.045 on the stressed word, once per line.
- **First frame** [I]: frame 0 is a finished composition. *Reel 08 fails: frame 0 is an empty board at 55% scale with faces half off-screen.*
- **Curiosity** [S]: curiosity needs a visible gap between what's known and wanted [10]. Across 600,000+ reading sessions, anxious, hopeful and exciting language held attention and sad language lost it. Certainty earned shares, not attention [11]. **Rule** [I]: uncertain hook, certain payoff. Keep the gap on screen until then.
- **Progress cues** [W]: in surveys, progress bars help only when early progress feels fast [12]. No video study found. **Rule** [I]: no full-length bar; step dots only inside the fix section. Keep section pills.
- **Loop** [F]: the last frame matches frame 0.
- **Text speed** [S]: viewers keep up with subtitles up to 20 characters/s [13]. **Rule:** karaoke chunk ≤4 words, ≤20 chars/s, ≥0.5 s.
- **Mayer's principles** [S], median effect sizes from lab studies, via secondary tables [14]:
  - Coherence, 0.86: no decoration beyond the spoken idea.
  - Signaling, 0.70 (independent meta-analysis: 0.38 [15]): pill words; dim older items.
  - Segmenting, 0.67: one board per section.
  - Redundancy, 0.10: no sentences on the board during speech. But 2–3-word labels on the graphic improved recall [16].
  - **Rule:** labels ≤3 words; ≤7 readable words and one hero number per board state.

## 3. Sound without licensed music
- **Speaker swaps** [S, radio]: sound effects and voice changes trigger orienting responses. Listeners habituate to repeated effects but not to voice changes [17]. Nobody talks over 6 s.
- **Muted viewing** [S]: muted reels are less visible [2], so the track is never silent. Every beat must still read with sound off [F].
- **Balance** [S]: listening tests recommend commentary ≥10 LU above music, ≥15 LU above ambience [18]. **Rule:** bed ≥15 LU under voice; SFX peaks ≥6 dB under voice peaks [F].
- **Too much** [F]: over one SFX per second, or an SFX with no visual event.

Numpy recipes:
- **Thump** (frame 0, payoff): sine 138→48 Hz sweep, 0.45 s.
- **Pop** (new element): sine chirp, 5 pitches; skip within 0.4 s of another SFX.
- **Whoosh** (section whips): noise through a band-pass sweeping 400→3,000 Hz.
- **Riser** (0.7 s before the payoff): noise through a band-pass rising 300→4,000 Hz, plus a 200→800 Hz sine, gain t². Then 0.3–0.4 s of silence.
- **Tick** (count-ups): 4 ms high-passed noise burst every 3 frames, −18 dB.

## 4. Colour and composition
- **Palette** [F]: paper, ink and one accent per board state. Blue is Aman, pink is Riya; red and green only mean bad and good.
- **Not a text slide** [S]: mostly-text reels are down-ranked [2]. Show objects, not word lists.
- **Type** [F]: read-me text ≥40 px. Raise the 26 px section pill to 34.
- **Gaze** [S, banner ads]: a face looking toward the product pulls attention there; direct gaze holds it on the face [19]. The speaker faces camera at hook and CTA; the listener looks at the board.
- **Safe zones** [W]: Meta's Reels ad guidance is top 269 px, bottom 672 px, sides 65 px, per third-party guides [20]. *Both our faces sit inside the bottom band.* Check the in-app preview.
- **Background** [I]: keep dot drift ≤0.4 px/frame; freeze it during count-ups.

## 5. Emotion and relatability
- **Sharing** [S]: across ~7,000 NYT articles, awe, anger and anxiety raised sharing and sadness lowered it. Useful and surprising pieces were shared more [21].
- **Loss vs gain** [S]: negative headline words raised click-through [22]. But across 165 effect sizes, loss-framed appeals were no more persuasive than gain-framed [23]. **Rule** [I]: hook on the loss, CTA on the gain.
- **Reactions** [I]: the listener is static today. A shock, laugh or facepalm lands within 6 frames of its trigger word.
- **"That's me"** [I]: show the mistake as Riya's action (her cursor heading for PAUSE).

**CTA** [S]. Instagram named "asking people to comment with a specific word, number, or emoji" as engagement bait, then clarified in June 2024 [6]:
- "Earnestly engaging with your audience in the comments and DMs to connect personally, generate leads" is not bait, and creators "can still use 3rd party services such as ManyChat".
- Bait is aiming "to simply maximize the quantity of engagements as a way to 'hack' reach".

No newer guidance found. Rules:
1. The keyword delivers a real thing by DM. Say what.
2. Never "comment YES", "tag 3 friends" or "like for part 2".
3. Add an open question: "Comment OCTOBER and your biggest ad worry."
4. The share prompt names a person [F]: "Send this to the friend about to pause their ads."
5. Save prompts need a save-worthy frame held ≥1.5 s [F].

## 6. QA checklist
1. First spoken word by frame 6.
2. Frame 0: board ≥95% scale, both faces fully in frame.
3. Hook claim (≤7 words) readable by frame 15.
4. ≥3 board-level changes in the first 3 s.
5. Gap between board-level changes ≤4 s; never over 2 per second.
6. No speaker holds over 6 s without a swap or reaction.
7. ≥4 listener reactions, each ≤6 frames after its trigger.
8. Karaoke chunk ≤4 words, ≤20 chars/s, ≥0.5 s.
9. ≤7 readable words per board state; labels ≤3 words.
10. Elements land within ±3 frames of their word.
11. Read-me text ≥40 px.
12. No text above y 269, below y 1248 or within 65 px of the sides.
13. Master −14 LUFS ±0.5; true peak ≤−1.5 dBTP.
14. Bed ≥15 LU under voice; SFX peaks ≥6 dB under voice.
15. ≤25 SFX per 50 s, each on a visual event.
16. One 0.3–0.4 s silence before the payoff; no other dead air over 0.3 s.
17. Muted stills make hook, mistake, answer and CTA clear.

## 7. Engine upgrades, by priority
1. **Finished frame 0.** Full board, both faces, claim readable. *Why:* skip rate is set in 3 s [4]. *Build:* `Reel.tsx`: run hook springs from `frame + 10` and scale 1.12→1, not 0.55→1; same for the `HookPrice` title and bust `enter`.
2. **Listener reactions.** Riya gasps, laughs, facepalms. *Why:* speaker changes don't habituate [17]. *Build:* `faces.py` adds `shock/laugh/facepalm` frames; `Bust` reads `pose` (already in `timeline.lines`) for 24 frames with a squash, scaleY 0.94→1.03→1.
3. **Payoff sound.** Riser, a breath of silence, then a bass hit. *Why:* onsets cue orienting [17]. *Build:* `voice.py` `riser()`; `script.json` `"payoff":"l9"` and `pauseBeforeMs: 350`, inserted as zeros before Whisper re-aligns; `thump` on the beat.
4. **Pill-word punch-in.** The board pushes in on highlighted words. *Why:* orienting [9]; signaling [14]. *Build:* board scale × `1 + 0.045 × spring({damping: 9, stiffness: 240})`, decaying over 12 frames, at each `tokens[].pill` time.
5. **Ducking and SFX budget.** Clear voice; no stacked pops. *Why:* 15 LU rule [18]. *Build:* `voice.py`: `bed *= 1 − 0.6 × smoothed env`; skip pops within 0.4 s of another SFX; print bed-vs-voice LU.
6. **Automatic QA report.** *Why:* enforces section 6. *Build:* `scripts/qa.mjs` computes checks 1, 4–10 and 15–16 from `timeline.json`.
7. **Open-loop chip.** A "?" stays between the clashing numbers until the payoff ticks it. *Why:* information gap [10]. *Build:* `views.tsx`: a `loop` item pinned from the hook to the `payoff` beat.
8. **Focus dimming and gaze.** *Why:* signaling [14]; gaze [19]. *Build:* opacity 0.6 on items older than the active beat; `Bust` leans 3° toward the board while listening.
9. **Ad-safe layout.** *Why:* safe zone [20]. *Build:* `theme.ts` `ad` variant: shrink `board.h` and lift bubble and busts until mouths (now y≈1500) clear y 1248.

## Sources
1. Social Samosa, 23 Jan 2025: https://www.socialsamosa.com/news-2/instagram-reveals-key-factors-for-boosting-reach-8646916
2. Instagram, 31 May 2023: https://about.instagram.com/blog/announcements/instagram-ranking-explained
3. Social Samosa, 25 Aug 2025: https://www.socialsamosa.com/news-2/instagram-retention-chart-skip-rate-new-performance-metrics-reels-9730992
4. Meta, 3 Dec 2025: https://developers.facebook.com/blog/post/2025/12/03/instragram-api-updates/
5. Instagram Creators, 30 Apr 2024: https://creators.instagram.com/recommendations-and-originality
6. Social Media Today, 5 Jun 2024: https://www.socialmediatoday.com/news/instagram-clarifies-advice-on-single-word-ctas-and-longer-reels/718151/
7. Om Malik, 1 Jan 2026: https://om.co/2026/01/01/what-is-instagrams-adam-mosseri-really-saying-in-his-year-end-memo/
8. Dost & Huang, 2026: https://archives.marketing-trends-congress.com/2026/pages/PDF/paper_professor_DOST_HUANG.pdf
9. Lang, 2000: https://doi.org/10.1111/j.1460-2466.2000.tb02833.x
10. Loewenstein, 1994 (cited from memory): https://doi.org/10.1037/0033-2909.116.1.75
11. Berger et al., 21 Mar 2023: https://www.ama.org/2023/03/21/the-challenge-of-keeping-an-audience-engaged-how-language-shapes-attention/
12. Conrad et al., 2003: https://rti.org/publication/effectiveness-progress-indicators-web-surveys-front-counts
13. Szarkowska & Gerber-Morón, 2018: https://doi.org/10.1371/journal.pone.0199331
14. Mayer 2021, via UNH handout, 2023 (figures via search): https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf
15. Alpizar et al., 2020: https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/A-meta-analysis-of-signaling-principle-in/99900601052901842
16. Mayer & Johnson, 2008: https://doi.org/10.1037/0022-0663.100.2.380
17. Potter et al., 2018: https://journalofcognition.org/articles/10.5334/joc.43
18. Torcoli et al., 2019, via arXiv: https://arxiv.org/pdf/2305.19100
19. Sajjacholapunt & Ball, 2014: https://pmc.ncbi.nlm.nih.gov/articles/PMC3941030
20. Hopper HQ, 2026: https://www.hopperhq.com/blog/instagram-reel-size/
21. Berger & Milkman, 2012: https://faculty.wharton.upenn.edu/wp-content/uploads/2011/11/Virality.pdf
22. Robertson et al., 2023: https://doi.org/10.1038/s41562-023-01538-4
23. O'Keefe & Jensen, 2006: https://typeset.io/pdf/the-advantages-of-compliance-or-the-disadvantages-of-40jafv9av1.pdf

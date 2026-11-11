---
name: reel-pipeline
description: The content pipeline for a batch of explainer reels — trend and topic research, a set of three with different jobs (news, relatable pain, seasonal), scripts, an independent fact and edit approval, free draft build, paid voice only after approval, render, QA and a posting kit. Use when asked for new reels, "what should we post", content research, or a weekly batch for a brand or agency account.
---

# Reel pipeline

Each stage writes a file the next one reads, so nothing depends on chat memory. Folder per batch: `docs/pipeline/<YYYY-MM-DD>/`. Build with the `explainer-module` skill; check delivery with `meta-delivery-qa`.

| # | Stage | Who | Output |
|---|---|---|---|
| 1 | Topic research | research agent, web search | `01-research.md`: 9–10 candidates, sourced facts, the viewer's wrong belief, an analogy, CTA idea, scores |
| 2 | Scripts | you (you know the engine) | `reel-N.script.json` per reel |
| 3 | Approval | a fresh agent that did not write them | `03-approval.md` + `reel-N.approved.json`: every claim VERIFIED / PARTLY / UNVERIFIED with URL + date, plus an edit pass |
| 4 | Draft build | you, free edge-tts voice | contact sheets + `qa_report.py`; fix layout and pacing here |
| 5 | Voice | one ElevenLabs v4 dialogue call per reel | `script/dialogue.mp3` (paid: only after 3 and 4 are clean) |
| 6 | Render + gate | you | MP4, cover, spec check PASS |
| 7 | Posting kit | you | `POSTING.md`: caption, pinned comment, auto-DM text, cover, when to post |

## 1. Research brief (what to ask for)
- A **set with different jobs**: one NEWS/AI hook from the last ~2 weeks (the format with proven reach on the founder's account), one RELATABLE mistake nearly every small advertiser makes, one SEASONAL action tied to the calendar this week.
- Per candidate: why now, 2–4 facts with URL + date actually seen, what the viewer wrongly believes (the student's line), a daily-life analogy, a keyword + the specific free thing sent by DM, 1–5 scores (relatability, useful today, novelty, explainable in 45 s, lead potential).
- Hard rules: never invent numbers; mark UNVERIFIED; official sources for platform facts; say when a search-volume tool had no data instead of guessing. Exclude topics already posted (list them).

## 2. Writing the scripts
Follow `explainer-module` (script rules + `references/`). Pick by evidence, not taste: the research scores plus what the account's own numbers say. Write the board at the same time as the lines: if a line has nothing to show, cut the line.

## 3. Approval brief
A skeptical fact-checker first, a short-form editor second. It must (a) verify each spoken, captioned or shown claim against a primary or reputable source and fix or remove anything not verified, (b) keep "reported by" framing where the platform has not published the claim itself, (c) check hook, wrong-belief line, analogy, ≤ 2 spoken numbers, payoff position, CTA wording, no guarantees or bait, (d) write fixed JSON with every cue still pointing at a spoken word. Never spend voice credits before this file exists.

## 4–6. Build
Draft with `scripts/draft_voice.py`, read every contact sheet, clear `qa_report.py`, then the real voice and the render. Countdown reels: rerun `voice.py` on the posting day.

## 7. Posting kit
Caption (hook line first, the receipt, the keyword and what it delivers, 5–8 hashtags), a pinned comment, the auto-DM text for the keyword (ManyChat or Meta Business Suite automations: without it comments don't become leads), the cover frame, the AI label reminder, and a posting slot per reel.

## Honest limits
No one can promise a reel goes viral. What this pipeline controls: a topic people already care about this week, a hook that reads in two seconds, a conversation people recognise themselves in, pacing inside known attention limits, facts that survive a check, and a CTA that turns comments into DMs. Measure skip rate, retention slope and sends per reach after 48 h and feed the result into the next batch.

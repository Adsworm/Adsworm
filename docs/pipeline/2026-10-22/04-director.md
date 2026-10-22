# 04 Director (22 Oct 2026)

Finals: `reel-A.final.json` and `reel-B.final.json`, 124 words each. No new facts. Every line except one per reel now has a beat (14 each), so the card changes about every ≤3 s. The `chip` delays are timed to land on the word they support. The comment card stays up to the last frame.

## Reel A

| # | Line (short) | Tone | Card | Note |
|---|---|---|---|---|
| 1 | Ads feel expensive? …+12% | knowing; hit "twelve" | Cover +12%; source chip ~1.8 s | Starts on the pain |
| 2 | R: October slow? | worried | {days} days to Diwali | Deadline by ~5 s |
| 3 | Partly… before Diwali | open loop | date chips | |
| 4 | CPM = 1,000 ad views | teacherly | CPM; 2024 chip ~2 s | Jargon defined |
| 5 | BF week +59% | firm | bars; "not India data" ~1.8 s | |
| 6 | R: Pause till Diwali? | anxious | red PAUSE ADS? | Viewer's doubt |
| 7 | No… −20% | short "No." | green −20% | Red→green turn |
| 8 | R: Wait, how? Ads cost more! | surprised | "Same week: CPM +59%" | NEW: bridges the paradox |
| 9 | Conversion +48% | explaining | bar + "ready to buy" ~2.2 s | |
| 10 | R: What do I actually fix? | practical | ✕ Only cut spend | |
| 11–12 | Don't just cut spend. / Fix after the click. | warning → confident | ✓ lands on line 12 | SPLIT so ✓ matches the voice |
| 13 | Offer, page, checkout | counting | steps, stagger 24 | Concrete |
| 14 | Comment OCTOBER… free | inviting | comment types OCTOBER + 4 check items | |
| 15 | R: Doing that before Diwali! | bright | + "Free… sent by DM" | Keyword stays visible |

**Voice:** direction prompt is in the JSON. gapCap 0.24, tempo 1.04. The script is dense with numbers, so they need room.
**Sound:** bedGain 0.07. The pad has no beat, so turning it up only adds mud. fxGain 0.8, because there are 14 pops now instead of 10 and lighter pops avoid click fatigue.
**Cover:** "WHY ADS FEEL EXPENSIVE" with a big +12%, "average price per ad · Q2 2026 vs Q2 2025", and the caption "…price per ad +12%".
**Risks:** (1) An abstract stat in the hook, so I put the pain question first. (2) Jargon on lines 4–5, so the definition is spoken and the chips land mid-line. (3) The CPM-up/cost-down contradiction, so I added Riya's "how?". (4) The unspoken 84% day bar could confuse. It's red and labelled "day"; drop it if QA flags it.


## Reel B

| # | Line (short) | Tone | Card | Note |
|---|---|---|---|---|
| 1 | Running Meta ads? Meta has told advertisers… 28th | calm urgency; stress date | Cover 28 OCT + {days} days; notice chip on "told advertisers" | Who it affects, then the date. Framing kept |
| 2 | Notice, not public announcement | matter-of-fact | ppc.land browser | MOVED before Riya |
| 3 | R: Wait, change my ads how? | surprised | browser note | Answered right after the cut |
| 4 | Adds product browsing | quoting | notice quote + receipt | |
| 5 | Tap may open product info | explaining, "may" | phone + flow chips | |
| 6 | R: Before my website? Good or bad? | worried | steps → "Your website: not first" | |
| 7 | Meta's test: +3% | neutral | green +3%; test chip ~1.8 s | |
| 8 | R: Conversions meaning sales? | sceptical | "Conversions = sales? sign-ups?" | NEW: viewer's question |
| 9 | It didn't say. Meta's own number. | honest | "Not defined" receipt + Help Center chip | Same claim, shorter |
| 10 | R: So what should I do? | ready | 3 OPTIONS | Signals the payoff |
| 11 | Opt out in one go, before 28th | clear | ALL ADS + "Before 28 Oct" | One view per option |
| 12 | Ad by ad, anytime | lighter; "anytime" | AD BY AD + settings path | No false urgency |
| 13 | Keep on a few, compare | practical | test steps | |
| 14 | Comment BROWSE… free | warm invite | comment UI + what we check | |
| 15 | R: Checking mine today! | upbeat | + "Free… sent by DM" | Keyword stays visible |

**Voice:** gapCap 0.22, tempo 1.05. It's news with fewer numbers, so it can move faster.
**Sound:** bedGain 0.07, for the same reason as A. fxGain 0.85, slightly crisper, which suits news.
**Cover:** "META'S NOTICE TO ADVERTISERS" with a big 28 OCT, "product browsing on existing ads", "6 days until 28 Oct", and the caption "Meta has told advertisers… live ads… 28 Oct".
**Risks:** (1) "Notice, not announcement" sounded like a dodge right after Riya's "how?", so I reordered it. (2) +3% reads as a win, so the "not defined" point follows within 2 s. (3) Three Aman instructions in a row, so each one gets its own big view. (4) The hook caption was too long, so I cut the caption to 60 characters. The spoken line is unchanged.


**Before render:** the `say` lines changed, so regenerate both dialogues. After running voice, check that no line runs past ~4.5 s. B's phone view is ~550 px tall in a 540 px slot, the same as the approved version, so check it on the QA sheet.

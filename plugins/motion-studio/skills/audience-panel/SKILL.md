---
name: audience-panel
description: Comprehension gate for a reel script before any voice or render. A fresh agent plays the audience (eight viewer types standing in for 10,000 viewers) and hears the script once; a second agent rewrites what was not understood; a new judge hears it again. Loop until it passes. Use for every explainer reel, and whenever the owner says a reel was "not clear" or "samajh nahi aaya".
---

# Audience panel (comprehension loop)

The fact check asks "is it true?". This asks "did they get it?". A script can pass the first and fail the second: three Hinglish reels did, on 13 Nov 2026.

## Loop
1. **Viewing sheet.** Write the script as the viewer meets it: one row per spoken line, with the time, the exact spoken words, and one plain sentence on what the screen shows. Nothing else: no title, no sources, no notes on what it "means". File: `docs/pipeline/<date>/panel/<slug>-v<N>.view.md`.
2. **Judge** (fresh agent, sees only the viewing sheet and the brief below). Output: `…-v<N>.judge.md`.
3. If FAIL: **Rewriter** (another agent; sees the sheet, the judge's report, the fact sheet and the writing rules). Output: the next viewing sheet.
4. A **new** judge reads the new sheet. Never reuse a judge: one that has seen an earlier version already knows what the reel is trying to say.
5. Stop at PASS, or after 4 rounds: then the idea is the problem, not the wording. Cut the topic in two or pick another.
6. After PASS, compare the judges' retellings with the message you intended. If they retell something else, it is still a fail.

## Pass mark
- Weighted understanding ≥ 85 (YES = full weight, PARTLY = half).
- Viewers 1, 2, 5 and 7 (the non-experts) each reach at least PARTLY and name the right action. For a viewer who has never run an ad, saving the video for the day they do counts.
- No single line confuses viewers worth 25 or more of the weight. A line confuses a viewer only if they cannot say what it meant; a name they do not need is not confusion when the sentence around it is understood.
- Viewers worth ≥ 70 are still watching after 5 seconds.

## Judge brief (send as written; fill only the file path)
> You are a test audience, not an editor. Read ONE file: `<path>`. It is the script of a short Instagram video, exactly as a viewer meets it: each row is what is SAID and what is ON SCREEN at that moment. Do not open any other file and do not search the web.
>
> Play these eight viewers, one at a time. Together they stand for 10,000 people who will see this video in India. The number is each type's share of that audience.
> 1. (20) Salon or boutique owner in a tier-2 city. Hindi first. Has pressed "Boost post" in the Instagram app. Has never opened Ads Manager.
> 2. (15) Clinic or coaching-centre owner. Pays an agency or a relative to run ads. Knows the word "leads". Does not know ad terms.
> 3. (15) D2C founder who runs their own Meta ads. Knows campaign, ad set, ROAS. Comfortable in English.
> 4. (10) Freelance media buyer. Expert.
> 5. (15) Sells from home (sarees, bakery) on Instagram and WhatsApp. Has never run an ad.
> 6. (10) Marketing student learning ads.
> 7. (10) Shop owner, 45+, little English. Watches reels with sound on. The page was set up by their son.
> 8. (5) Not in business. Just scrolling.
>
> Rules of watching: each viewer hears every line ONCE, at speaking speed, and cannot go back. A word they have never heard is not understood unless the same sentence explains it. A comparison only works if it is obvious what stands for what. Two confusing lines in a row and attention goes. The first five seconds decide whether they stay. Be the viewer you are given, not a clever reader: if you would have to stop and think, the viewer did not get it.
>
> For each viewer give: (a) the second they scroll away, or "till the end"; (b) what they think the video said, in one sentence in their own words and at their own level; (c) what they would do after watching; (d) the exact words or lines they did not get; (e) UNDERSTOOD: YES / PARTLY / NO.
>
> Then give: the weighted score (YES = full weight, PARTLY = half, NO = 0; show the sum); the lines that lost people, worst first, with the viewers and the weight lost; every term that was used without being explained; whether it is too fast or carries too many ideas; and whether the picture on screen helped or fought the words, line by line where it matters. Finish with VERDICT: PASS or FAIL against this bar: score ≥ 85; viewers 1, 2, 5 and 7 each at least PARTLY with the right action (for a viewer who has never run an ad, saving the video for the day they do counts); no line confusing viewers worth ≥ 25 (a line confuses a viewer only if they cannot say what it meant); viewers worth ≥ 70 still watching after 5 seconds. Do not rewrite the script. Do not be kind. Under 700 words.

## Rewriter brief (send as written; fill the paths)
> You rewrite a short Hinglish video script so that ordinary Indian business owners understand it on one hearing. Read: the current script `<view path>`, the audience test report `<judge path>`, the facts you may use `<facts path>`, and the writing rules in `plugins/motion-studio/skills/audience-panel/SKILL.md` (section "Writing rules"). Do not search the web. Do not add any fact, number or claim that is not in the facts file; you may drop facts.
>
> Fix every line the report says lost people. Keep what worked. Then write the new viewing sheet to `<next view path>` in exactly the same table format (time, speaker, spoken words in Roman Hinglish, on screen), and reply with: the full new script, and a short list of what you changed and which finding each change answers. Do not judge your own rewrite.

## Writing rules (comprehension first)
1. **One message per reel**, said plainly in the first 8 seconds and said again at the end in almost the same words.
2. **One narrator talking to "aap".** Whole spoken sentences, the way you would explain it to a shop owner across the counter. No fragments ("Tha.", "Wahi bheed, teen baar.").
3. **At most one new term per reel**, and the same sentence says what it is ("Andromeda, yaani Meta ka wo system jo…"). Words like ad set, conversion, campaign type, learning, creative, broad: replace with plain words or do not use.
4. **Show the thing itself, not a stand-in.** Use the viewer's own world (their ad, their customer, their phone). At most one comparison, and say both halves out loud ("jaise…, waise hi…").
5. **Three beats:** what you have heard or what happened → what it really is → the one thing to do. One action only.
6. **The screen repeats the sentence**, in fewer words. It never adds a second idea.
7. **Numbers:** at most two spoken, rounded, with what they count.
8. 100–125 spoken words, 45–58 s. Never speed the voice up to fit: cut words.
9. Hinglish the way Delhi speaks: Hindi grammar, English only for words people already use in English (ad, account, comment, offer, customer, review).

## What the first run taught (Andromeda reel, 13 Nov 2026: 60 → 82.5 → 90 → pass)
- **Open in the viewer's world, not on the trend word.** "Aapka business Instagram par hai?" kept 95 of 100 past 5 s; opening on "Andromeda 2.0" lost a fifth. Put the trend word on screen, in the caption and as the comment keyword instead.
- **The action goes in the first 8 seconds** and again at the end. "Nothing to do" early lets people leave.
- **Cut every line that is only interesting.** "The machine got faster" and the expert rumour were the two failing lines.
- **Say what "the same" means** ("wahi photo, wahi baat") and say the cost out loud ("kam logon tak pahunchta hai"); a picture alone did not carry either.
- **The closing promise must be a thing**: "teeno ads ke ready namoone", not "the company's own words".
- **Screen text:** the key message in Devanagari (three words), no ticks beside "no" sentences, no long notes while someone is talking. Mark ad cards "Ad" or they read as ordinary posts.
- A reel that passes for owners will bore experts. That is the trade; pick the audience before writing.

## Limits
The panel is a simulation by a language model. It catches missing explanations, jargon and overloaded lines; it cannot hear the voice. Accent, pronunciation and caption sync are checked separately (voice samples for the owner's ear, forced alignment for timing).

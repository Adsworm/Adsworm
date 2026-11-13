# 05 Comprehension loop: the Andromeda reel, rewritten until an audience panel understood it (13 Nov 2026)

**Why:** the owner rejected all three Hinglish reels: "samajh nahi aa raha" (words not matching the voice, the female voice, Hindi ↔ English switches, the mannequin analogy, the concept itself). Three separate faults were found and each has its own fix:

| Fault | Evidence | Fix |
|---|---|---|
| Script too compressed, analogy needs decoding | Panel round 1 scored 60/100 | Audience-panel loop (below); one narrator, one message, the screen shows the thing itself |
| Captions out of step with the voice | Measured on a Hinglish clip with known word times: 126 ms average error, more than 150 ms for 1 word in 5 | Word times now come from the voice engine itself (`<audio>.words.json`): 119 of 119 exact in the draft |
| Voices are not native Hindi speakers | Higgsfield has 114 preset voices: no Indian male name, one possibly Indian female (Anika) | A Hinglish-native voice service (see `04-tools.md`); needs the owner's API key or a recording of his own voice |

## The loop (skill: `plugins/motion-studio/skills/audience-panel`)
A judge agent plays eight viewer types standing for 10,000 viewers and hears the script once. Another agent rewrites. A new judge, who has seen nothing before, hears the new version. Pass mark: 85.

| Round | Version | Score | What the judge said |
|---|---|---|---|
| 1 | v1 (mine) | 60 FAIL | Opens on an unknown word and a rumour most never heard; "ad account" heard as the Instagram account; the action arrives at 30 s |
| 2 | v2 (rewriter) | 82.5 FAIL | Much plainer. Two extra lines still lose people: "the machine got faster" and "do not rebuild your account" |
| 3 | v3 (rewriter) | 90, FAIL on one bar | Message lines clean. The closing promise ("Instagram wali company ki apni baat") meant nothing to viewers worth 45 |
| 3 | v3b (trend word first) | 75 FAIL | Opening on "Andromeda 2.0" lost the home seller and the scroller in 5 s. **The trend word in line 1 costs about a fifth of this audience** |
| 4 | v4 | **90 PASS** | All four non-expert viewers understood and named the right action. Margin is thin: one viewer short of failing |

After the pass, two notes from the last judge were applied without another round: every ad card carries a small "Ad" mark (cards were being read as ordinary posts), and the closing promise sends "ready namoone" instead of repeating the three ideas.

What the panel's viewers said the reel told them (round 4): "Boost ya ad ek jaisa baar-baar mat chalao; kaam, tareef, offer alag-alag, warna kam log dekhenge." That is the intended message.

## Final script, line by line (119 words, 53 s)
| # | Voice text (Hindi in Devanagari, English in Latin) | Caption (Roman Hinglish) | On screen |
|---|---|---|---|
| 1 | आपका business Instagram पर है? | Aapka business Instagram par hai? | Phone par ek dukaan ka Instagram page |
| 2 | तो एक बात याद रखिए: हर ad अलग बनाइए. | Toh ek baat yaad rakhiye: har ad alag banaiye. | Teen alag ad cards + bada text: हर ऐड अलग |
| 3 | Instagram पर किसे कौन-से ads दिखें, ये एक machine छाँटती है. | Instagram par kise kaun-se ads dikhein, ye ek machine chhaant-ti hai. | Ads ka dher → ek machine (box) → kuch hi ads → ek insaan |
| 4 | आजकल लोग इसे Andromeda टू-पॉइंट-ओ कह रहे हैं. | Aajkal log ise Andromeda 2.0 keh rahe hain. | Box par naam aata hai: ANDROMEDA 2.0 / एंड्रोमेडा 2.0 |
| 5 | आपके ads एक जैसे हुए, वही photo, वही बात, | Aapke ads ek jaise hue, wahi photo, wahi baat, | Paanch ad cards, sab mein wahi photo |
| 6 | तो ये machine उन्हें एक ही ad समझ सकती है. | toh ye machine unhe ek hi ad samajh sakti hai. | "=" ka nishaan, uske baad ek hi card |
| 7 | फिर आपका ad कम लोगों तक पहुँचता है. | Phir aapka ad kam logon tak pahunchta hai. | Ek card, saamne bheed, sirf do log roshan |
| 8 | इसलिए एक ad में अपना सामान या काम दिखाइए. | Isliye ek ad mein apna saamaan ya kaam dikhaiye. | Pehla card: saamaan ya kaam → ek insaan |
| 9 | दूसरे में customer की तारीफ़, तीसरे में offer. | Doosre mein customer ki tareef, teesre mein offer. | Doosra card (tareef) aur teesra (offer) → alag-alag log |
| 10 | Post को पैसे देकर आगे बढ़ाते हैं, यानी boost? वो भी ad ही है. | Post ko paise dekar aage badhate hain, yaani boost? Wo bhi ad hi hai. | Phone par "Boost post" button dabta hai, sikka girta hai, post aur phones tak jaati hai |
| 11 | अभी ad नहीं चलाते? ये video save कर लीजिए. | Abhi ad nahin chalate? Ye video save kar lijiye. | Save ka nishaan dabta hai aur bhar jata hai |
| 12 | याद रखिए: हर ad अलग बनाइए. | Yaad rakhiye: har ad alag banaiye. | Phir se: हर ऐड अलग |
| 13 | Comment में ANDROMEDA लिखिए. | Comment mein "ANDROMEDA" likhiye. | Comment box mein bade aksharon mein ANDROMEDA type hota hai |
| 14 | तीनों ads के ready नमूने, Hindi में, भेज दूँगा. | Teeno ads ke ready namoone, Hindi mein, bhej dunga. | Neeche Hindi mein message girta hai: तीनों ads के ready नमूने |

## Limits (said plainly)
- The panel is a language model playing viewers. It catches jargon, missing explanations and overloaded lines. It is not real viewers, and it cannot hear.
- The draft video uses a free draft voice that may not be published (Microsoft's terms; `04-tools.md` A3). It is there to judge the script, the pictures and the caption sync.
- A media buyer or D2C founder finds this reel basic (the judge said so each round). It is written for owners who boost posts or have an agency run their ads.

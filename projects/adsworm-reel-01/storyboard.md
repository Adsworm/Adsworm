# FULL CHAIRS 01: "1 → 15", second-by-second storyboard

- **Status:** the creative-director agent approved the plan (8 required changes applied), then reviewed the built frames (3 fixes applied: Meta-compliant ad copy, hierarchy, end-card timing).
- **Format:** 1080×1920, 30 fps, 1020 frames (34.0 s).
- **Tempo:** 120 BPM, so 1 beat = 15 f and 1 bar = 60 f = 2 s.
- **Safe area:** text stays inside y 269–1248 and x 65–1015.
- **Palette:** ink `#0B0B0C` background, paper `#F4F2EE` text, lime `#C8FF2E` accent, muted `#8A8A8F`.
- **Type:** Inter Tight 800 for display, Instrument Serif italic for the emotional word.

The single source of truth is `src/reel/timeline.json`. Both the scenes and `scripts/sound.py` read it.

| Sec | Frames | Bar | On screen (exact copy) | Motion | Sound |
|---|---|---|---|---|---|
| 0 | 0–29 | 1 | Clinic icon + **"1 clinic."**, fully visible on f0. Tag "ADSWORM · FULL CHAIRS 01" (36 px, muted, y≈290) | Icon idle float. Frame 0 is the thumbnail | Pad + sub enter |
| 1 | 30–59 | 1 | **"15 branches."** ("15" in lime) | f30: the icon multiplies into a 3×5 grid (centre-out springs, 1 f stagger). Counter 1→15. "1 clinic." exits up, "15 branches." rises in | Impact f30, ticks f31–45 |
| 2 | 60–89 | 2 | "Same city." | Grid dims to 25%. Words rise from a mask | Pop f60 |
| 3 | 90–119 | 2 | "Here's what changed." | The series tag exits at f119 | Pop f90, whoosh f117 |
| 4 | 120–149 | 3 | "Most clinic ads look like this:" | One generic ad card springs up: grey photo block, red **FLAT 20% OFF**, "Hair PRP", "Clinic Name", blue "Book now" | Groove starts. Pop f126 |
| 5 | 150–179 | 3 | (card holds and is readable) | Idle float | — |
| 6 | 180–209 | 4 | "Every clinic. Same ad." | The card shrinks into a 3×3 grid. The treatment line varies (PRP / Laser / Whitening / HydraFacial / Skin Peel) | Whoosh f180, pops f182/188/194 |
| 7 | 210–239 | 4 | (grid holds) | Idle | — |
| 8 | 240–269 | 5 | "Patients scroll right past." | The grid desaturates to 35% | — |
| 9 | 270–299 | 5 | (same) | The grid flicks upward like a scroll (inExpo, 18 f) | Whoosh f270 |
| 10 | 300–329 | 6 | "Patients don't book discounts." | Kinetic words over ink | Break: pad + hats |
| 11 | 330–359 | 6 | (holds) | Ambient drift | — |
| 12 | 360–389 | 7 | "They book *certainty.*" ("certainty." in lime serif italic) | The accent word lands larger at f375 | Soft hit f375 |
| 13 | 390–419 | 7 | (holds) | — | — |
| 14 | 420–449 | 8 | "3 checks before your next ad" + **SAVE THIS** bookmark tag | The headline rises and the grey card returns at f435 | Groove. Pop f435 |
| 15 | 450–479 | 8 | (SAVE THIS pops) | Bookmark tag springs | Tick f450 |
| 16 | 480–509 | 9 | "① One treatment per ad" | Lime strike draws across "FLAT 20% OFF" (f495, 12 f), and the badge is gone by f520. From f480 the header and pill recede to 45% and 0.88×, so the numbered check is the only focal point | Pop f480, whoosh f495 |
| 17 | 510–539 | 9 | (holds) | — | — |
| 18 | 540–569 | 10 | "② Name the city. Name the problem." | The "PUNE" pin tag snaps onto the card at f555 | Pop f540, pop f555 |
| 19 | 570–599 | 10 | (card subline becomes "PRP for early thinning": no age or condition claims, per Meta's Personal Attributes policy) | Text swap at f570 | Tick f570 |
| 20 | 600–629 | 11 | "③ New creative every week" | The card fans into W1 · W2 · W3 (f615/620/625) | Pops |
| 21 | 630–659 | 11 | (fan holds) | — | — |
| 22 | 660–689 | 12 | **"30+"** + "clinics scaled across India." | The 15-icon grid returns and grows | Whoosh f660, ticks f675–717 |
| 23 | 690–719 | 12 | (counter 15 → 30) | Icons pop in | Ticks |
| 24 | 720–749 | 13 | "30+" lands (lime) | The counter lands on the downbeat f720 | Impact f720 |
| 25 | 750–779 | 13 | (holds) | — | — |
| 26 | 780–809 | 14 | "Want us to check your ads?" | Kinetic type | Break. Riser toward f840 |
| 27 | 810–839 | 14 | (holds) | — | Riser builds |
| 28 | 840–869 | 15 | "Comment **AUDIT**" | One spring pop (damping 12, no pulse). The comment field (y ≤ 1200) types A-U-D-I-T over f850–870 | Groove. Pop f840, type clicks |
| 29 | 870–899 | 15 | "Free 20-min teardown · Clinic owners only" | Send arrow turns lime at f876. The subline fades up at f870 | Tick f876, pop f870 |
| 30 | 900–944 | 16 | (CTA holds; 3.5 s in total) | Ambient | Whoosh f943 |
| 31.5 | 945–959 | 16–17 | ADSWORM logo | The filled logo wipes in left→right over 15 f. It is never shown as an outline (brand rule) | Impact f945 |
| 31.7 | 951–1011 | 17 | "@adsworm" (f951) · "The clinic growth agency" (f957) · muted "Made 100% in code." (f963) | Each line rises in and holds ≥ 1.6 s | Pops f951, f957 |
| 33.7 | 1012–1019 | 17 | → frame-0 state ("1 clinic.") | An 8-frame crossfade back to frame 0, so the reel loops | Tail fade |

## Caption

> Ads chal rahe hain. Chairs khaali kyun?
>
> 1 clinic → 15 branches. Same city. What changed wasn't the doctors. It was ads built for one treatment, one city and one real problem, refreshed every week.
>
> Clinic owners: comment **AUDIT** and we'll send you a free 20-minute teardown of your current ads.
>
> FULL CHAIRS · Episode 01. Save this for your next campaign.
>
> #clinicmarketing #dermatologyclinic #dentalclinic #hairclinic #metaads #clinicgrowth #adsworm

The caption is held until the owner confirms the 1→15 and 30+ claims.

**Pinned comment:** "The 3 checks: ① one treatment per ad ② name the city and the problem ③ new creative every week. Comment AUDIT for a teardown of yours."

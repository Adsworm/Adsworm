# Adsworm Instagram: audit, content plan and demo reel v1

Prepared 2026-10-21 for review. The reel will be built 100% in code (Remotion + the motion-studio skills). The music and SFX are synthesized in code as well. It uses no camera, no stock footage and no AI generation.

## 1. Audit of @adsworm

Data comes from the Meta Graph API through the connected Meta account: the last 25 posts.

| Signal | Finding |
|---|---|
| Cadence | The last post was 2026-06-29, which is 114 days of silence. Before that there was a 10-month gap (Aug 2025 → Jun 2026). Only 2 posts in the last 14 months |
| Engagement | Most posts get 6–29 likes and 0–4 comments. The best performer was the 2023-08-10 "bullseye" reel with 259 likes. The 2023-11-09 success-story reel got 54 likes and 20 comments |
| Positioning | Scattered across CGI videos (₹5k), AI miniatures (₹19,999), Shopify sites (₹16,999), TikTok, ChatGPT, AI avatars and clinic growth. The discount pricing fights the premium positioning |
| Strongest asset | The 2026-06 clinic posts carry specific proof: 1 clinic → 15 branches, 30+ clinics scaled, owner-to-owner tone. The ad-account portfolio confirms clinics are the core: skin and hair, dental and multi-city clinic chains, plus salons |
| What's missing | A consistent visual identity, a series format, educational value that earns saves and shares, and a CTA that creates comments |

The @amanrai.official account could not be audited: it isn't linked to the Meta Business, and Instagram blocks logged-out reads.

## 2. Positioning for the feed

**"The clinic growth agency."** Clinics are the core. Every post speaks to a clinic owner. Everything else (CGI, websites, AI content) moves to the highlights or to case studies.

## 3. Content system (all producible in code with motion-studio)

| Pillar | Format | Why it works | Engine |
|---|---|---|---|
| **Ad Teardown**: why a typical clinic ad fails, then the fix | 25–35 s reel | Authority, saves, shares to partners | Remotion kit + custom scenes |
| **Clinic Growth Math**: CPL → show-up → treatment value, animated | 20–30 s reel / carousel | Owners think in numbers. Highly saveable | Remotion (counters, charts) |
| **Proof Stories**: anonymised case motion (1 → 15 branches) | 30–40 s reel | Trust, inbound leads | Remotion |
| **Myth vs Fact**: fast kinetic type | 10–15 s reel | Comments and debate drive reach | Kit, variant matrix |
| **Made in Code**: "this reel is 100% code" showcase | 20 s reel | Differentiator; sells Adsworm's creative capability | Remotion / HyperFrames |
| **Carousels**: statics from the same props | 5–8 slides | Saves | `npm run stills` |

**Cadence:** 3 reels and 1 carousel a week. This is sustainable because every format is a parametric template. A new post means new copy and props, not a new edit.

**Series identity:**
- The same 0.5 s opening sting: logo mark, a lime bar and the series name.
- The same lime accent and type system.
- The same end card.

**CTA system:** "Comment AUDIT". Automate the DM replies with ManyChat or reply manually. Comments boost reach, and the DMs capture leads.

## 4. Demo reel v1: "1 → 15"

| Setting | Value |
|---|---|
| Objective | Profile-building plus inbound leads from clinic owners. Engagement through comments, saves and shares |
| Audience | Clinic owners and doctors (derm, dental, hair, aesthetic) running or considering Meta ads |
| Format | 9:16 1080×1920, 30 fps, **34 s**. Sound-off first (burned-in type carries everything). 120 BPM synthesized bed, so 1 bar = 2 s = 60 frames |
| Single message | Clinics don't need more ads, they need ads built for their city and their treatments, and Adsworm has scaled a clinic from 1 branch to 15 that way |

### Hook options (pick one)
- **A, contrarian:** "Your clinic doesn't need more ads." → "It needs different ones."
- **B, pain:** "₹1 lakh a month on ads. Chairs still empty?"
- **C, proof-first curiosity (recommended):** "1 clinic. 15 branches." → "Same doctors. Same city." → "Here's what changed."

### Beat structure (bars of 2 s)

| Bars | Time | Beat | On-screen copy (draft) | Motion idea |
|---|---|---|---|---|
| 1–2 | 0–4 s | Hook | "1 clinic." / "15 branches." / "Same doctors. Same city." | A single clinic icon on black multiplies into a 3×5 grid on the beat. The counter runs 1 → 15 |
| 3–5 | 4–10 s | Problem | "Most clinic ads look like this:" → a grid of identical ads ("FLAT 20% OFF hair PRP") → "Patients scroll past all of them." | Phone-frame ad cards repeat, then grey out and slide away |
| 6–8 | 10–16 s | Shift | "Patients don't book discounts." / "They book *certainty.*" | Kinetic type with a serif-italic accent in lime |
| 9–11 | 16–22 s | Mechanism | ① Treatment-level ads ② City-specific pain points ③ New creative every week | Three chips stack in, one per bar, with a check tick on the beat |
| 12–13 | 22–26 s | Proof | "30+ clinics scaled across India" | Counter 0 → 30+, with a dot field filling in |
| 14–15 | 26–30 s | CTA | "Want this for your clinic?" → "Comment **AUDIT**" → "Free 20-min teardown of your ads" | The comment-bubble UI types "AUDIT", and a lime CTA pulses |
| 16–17 | 30–34 s | End card | ADSWORM logo draw-on · @adsworm · "This reel is 100% code." | The SVG logo draws stroke-on, then fills |

### Sound (coded)
- **Bed:** 120 BPM minimal tech: kick on every beat, offbeat hats, sub bass on the bar, a soft pad.
- **SFX:** a tick on each counter step, a pop on each chip, a low impact on the 15-grid reveal, a typing click for "AUDIT", and a riser into the end card.
- **Mastering:** −14 LUFS and ≤ −1 dBTP, checked with `check_specs.sh`.

### Caption (draft)

> Same doctors. Same city. 1 clinic → 15 branches. The difference wasn't budget, it was ads built for *that* city and *those* treatments. Clinic owners: comment AUDIT and we'll send you a free 20-minute teardown of your current ads. (This reel was made 100% in code.)

Hashtags: 5–8 niche tags (#clinicmarketing #dermatologyclinic #dentalmarketing #metaads #clinicgrowth #adsworm).

### Success metrics (first 7 days)
- 3-s hold above the account's reel median.
- Comments ≥ 10, at least half of them "AUDIT".
- Saves plus shares ≥ 15.
- Profile visits and follows logged as a baseline for the series.

## 5. Risks
- **Claims** come from Adsworm's own captions (`brands/adsworm/claims.md`) and need owner confirmation. "3x in 60 days" is excluded as a guarantee.
- **Mock ad cards** must be visibly generic. Use no real clinic names or creatives.
- **The logo** was traced from the 1080 px profile picture. Swap in the master vector if one exists.
- **The "AUDIT" CTA** needs someone, or ManyChat, replying within hours.

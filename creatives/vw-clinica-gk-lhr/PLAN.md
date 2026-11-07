# VW Clinica — Greater Kailash — Full Body LHR creative rebuild

## Version 2 (premium) — current files: VWClinica_GK_LHR_PREMIUM_V1/V2/V3_1080.png

### Brand fonts, matched by measurement
Each text sample was cut out of the original creative and compared with 100+ Google Fonts renders (pixel overlap, IoU, plus a width penalty).
| Original text | Best match | Overlap |
|---|---|---|
| "Reduction" (headline) | Libre Caslon Text 700, tracking -0.06em | 0.715 |
| "19,999" (price digits) | Libre Caslon Text 700 (Ibarra Real Nova 700 scored 0.76) | 0.734 |
| "Greater Kailash Branch, New Delhi" | DM Sans 600 | 0.616 |
| "+91 81309 24067" | Figtree 600 / Inter 500 / DM Sans family | 0.63 |
The original looks image-model generated, so no exact font exists; the system uses one serif family (Libre Caslon Text) for headline and prices and one sans (DM Sans) for everything else.

### Hierarchy (measured on V1, 1080×1080, versus the original)
| Element | Original | Version 2 |
|---|---|---|
| Headline "Full Body Laser Hair Reduction" | 26.6% of height | 28.5% (112 px, 3 lines) |
| Price digits | 9.9% | 13.1% (152 px, full-width price menu) |
| Phone number | 2.9% | 3.1%, white on deep teal, own half of the contact bar |
| Location | 2.2% | 2.8%, serif "Greater Kailash" under "VISIT US" |

### Premium rules applied
- Two type families only; gold used only as hairlines and small caps, no filled gold bars, pills or badges.
- Price shown as a menu: label left (6 / 10 SESSIONS, small caps), price right, one hairline between rows.
- ₹ set at half size in champagne, top-aligned.
- Fewer elements: logo, eyebrow, headline, two price rows, location, phone.
- Same layout system for all three; the photo changes (clinic scene, treatment close-up, lifestyle) so Meta has three distinct creatives to test.

---

## Version 1 (superseded)

Offer kept as on the original creative: 6 sessions ₹19,999 · 10 sessions ₹29,999 · No-cost EMI.
Brand colours kept: deep teal #00434D, logo teal #31A1B0, gold #E3C27E / #F0DCA7, cream #FCF9F1.
Fonts changed (allowed): Playfair Display (headline, prices) + Montserrat (labels, location, phone).

## Measured issues on the original (1254×1254)
| Element | Size | Share of canvas | On a phone feed |
|---|---|---|---|
| Headline "Full Body Laser Hair Reduction" | 548×334 px | 26.6% height | ~104 pt |
| Price ₹19,999 | 124 px tall | 9.9% | ~39 pt |
| Phone number | 36 px tall | 2.9% | ~11 pt |
| Location line | 28 px tall | 2.2% | ~9 pt |
| "NO-COST EMI AVAILABLE" | 21 px tall | 1.7% | ~7 pt |
| "LIMITED PERIOD OFFER" | 21 px tall | 1.7% | ~7 pt |

Area split: photo + headline 62.2% · price panel 28.3% · contact strip 9.5%.
Contrast is fine (location 8.1:1, phone 10.3:1); the problem is size and position.

## What changed (all three variations)
- Contact zone 9.5% → 15.9% of the canvas: a cream location strip plus a full-width gold call bar.
- Phone digits 2.9% → 4.4% of the canvas height, heavy sans-serif, CALL / WHATSAPP label and icons.
- Location: bold strip with a pin (2.2% → 2.9%), plus "Greater Kailash" in the headline (V1) or a top badge (V2, V3).
- Price anchor: "BEST VALUE · UNDER ₹3,000/SESSION" on the 10-session plan (₹29,999 ÷ 10 = ₹2,999.9).
- No-cost EMI: thin line → bordered bold pill.
- Photography: patient and clinician both wear laser eye protection; premium South Delhi interior.

## Variations
- V1 Location-first — "Greater Kailash's Full Body Laser Hair Reduction"
- V2 Value — "Smooth skin at under ₹3,000 a session."
- V3 Lifestyle — "Smooth skin. Zero waxing."

## Photo prompts (Higgsfield, gpt_image_2_5, 1:1, 2k, high)
V1: Square 1:1 premium editorial photograph inside an upscale laser clinic in Greater Kailash, South Delhi. An elegant Indian woman in her early 30s with smooth glowing skin, wearing a sleeveless ivory silk top and wearing dark protective laser goggles, sits relaxed and smiling softly on a cream leather treatment chair. A female clinician in a crisp white tunic with deep teal (#00434D) piping and white nitrile gloves glides a sleek modern diode laser handpiece with a clear cooling tip along the woman's forearm. Behind them, a premium laser machine with a glowing touchscreen. Interior: warm travertine and ivory walls, brushed brass accents, a deep teal velvet cushion, soft natural daylight. Composition: both people and the machine sit in the RIGHT 55% of the frame, in the vertical middle band. The LEFT 45% is soft, calm, out-of-focus ivory wall. The TOP 20% and BOTTOM 35% of the whole frame must stay calm and uncluttered because text panels will cover them. Photorealistic, natural visible skin texture, 50mm lens, shallow depth of field, luxury clinic mood. No text, no letters, no numbers, no logos, no watermark.

V2: Square 1:1 premium close-up photograph for a luxury laser hair reduction clinic. A smooth, glowing, hair-free leg of an Indian woman (from knee to ankle) rests diagonally on a cream leather treatment bed; a clinician's hand in a white nitrile glove guides a sleek diode laser handpiece with a clear sapphire cooling tip just above the shin, a faint soft cool glow at the tip. A neatly folded deep teal (#00434D) towel lies at the edge of the bed. Background: warm ivory and travertine, completely out of focus. Composition: the leg and handpiece run diagonally across the RIGHT half and centre of the frame. The LEFT 45% and the TOP 25% of the frame are calm, empty, soft-focus ivory space. The BOTTOM 35% stays simple and uncluttered because a text panel will cover it. Clean luxury clinical lighting, natural skin texture, 85mm macro look, tasteful and non-explicit. No text, no letters, no numbers, no logos, no watermark.

V3: Square 1:1 luxury lifestyle portrait for a premium laser hair reduction clinic in South Delhi. A confident, elegant Indian woman around 30 with smooth, radiant, hair-free arms, wearing a sleeveless deep teal (#00434D) satin dress and small gold earrings, stands on a sunlit terrace of an upscale Greater Kailash home with lush green plants and warm cream walls. One hand gently tucks her hair behind her ear, arm relaxed, natural warm smile, golden-hour light with soft champagne highlights on her skin. She occupies the RIGHT 50% of the frame, from the waist up, facing slightly left. The LEFT 50% is softly blurred cream wall and greenery, calm and empty for text. The BOTTOM 35% of the frame stays calm and simple because a text panel will cover it. Editorial fashion photography, 85mm lens, shallow depth of field, natural skin texture. No text, no letters, no numbers, no logos, no watermark.

## Layout spec (1080×1080, text set in code, not by the image model)
- 0–628: photo + cream gradient; logo top-left (196 px wide); headline block on the left.
- 628–908: deep teal offer panel; two price columns (104 px Playfair 800), BEST VALUE tag, EMI pill.
- 908–976: cream location strip, pin + "GREATER KAILASH" (36 px Montserrat 800) + "New Delhi · VW Clinica".
- 976–1080: gold call bar, phone + WhatsApp icons, "+91 81309 24067" (68 px Montserrat 900).

## Open points
- The live Greater Kailash ad in the Ad Library is titled "5 Sessions ₹15,999 | Unlimited sessions for 1 year at just ₹31,999 – US-FDA Approved | GREATER KAILASH BRANCH". The creative shows 6 @ ₹19,999 / 10 @ ₹29,999 (the Noida and Faridabad offer). Confirm the GK offer and make the ad text match the image.
- Exact GK address (GK-I or GK-II, block, market, landmark) to add to the location strip.
- "US-FDA approved technology" is taken from VW Clinic's own GK ad title; confirm before publishing.
- The photos are AI-generated: mark the creative as AI-generated in Meta when publishing.

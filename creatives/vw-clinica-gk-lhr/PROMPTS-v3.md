# VW Clinica GK LHR — v3 flyers (full-render method)

Method (from research on tenfoldmarc/meta-ads-generator-skill and mrpaidsocial/uni1-image-ad): the image model renders the finished flyer, text included, with brand reference images, instead of a photo with code-overlaid text. Every output is then checked digit by digit.

- Model: Higgsfield gpt_image_2_5, 1:1, 2k, quality high (2.75 credits each).
- Reference 1: the original GK creative (palette and mood only, layout not copied).
- Reference 2: the VW CLINICA logo (reproduce exactly).

## Locked rules (appended to every prompt)
Prices exactly ₹19,999 and ₹29,999 with the Indian rupee sign; never 19999, 19.999, Rs, INR, $, 14,999 or 1,9999. Phone exactly +91 81309 24067; never change, add or drop a digit. Only two typefaces: a refined serif (Caslon / Playfair style) and a clean geometric sans (DM Sans style). Palette only deep teal #00434D, logo teal #31A1B0, champagne gold #D9BC85, warm cream #FCF9F1. Photorealistic, natural skin texture with visible pores, no airbrushed skin, 50-85mm full-frame lens look, soft diffused light, anatomically correct hands. No before/after, no split screen, no collage, no stickers, no extra words, no emojis, no URLs, no watermark, no phone UI. Nothing important within 40px of the edges.

## Variants (exact on-image text)
1. Price-first: client and clinician (both in laser goggles), forearm treatment. "Full Body Laser Hair Reduction" · "6 SESSIONS ₹19,999" · "10 SESSIONS ₹29,999" · "No-Cost EMI Available" · "Greater Kailash, New Delhi" · "+91 81309 24067".
2. Authority: clinician with premium laser machine, teal gradient, framed price card. Adds "US-FDA APPROVED TECHNOLOGY" (from VW Clinic's own GK ad title; confirm).
3. Outcome: woman in teal satin dress on a South Delhi terrace, cream price panel. Adds "Smooth skin, every season."
4. Proof: consultation lounge. Adds five stars + "TRUSTED BY 50,000+ CLIENTS" (from a 2025 VW Clinic ad title; confirm before running).

## QA done
- All four: prices, phone, location, EMI line and headline spelled exactly; logo matches the reference.
- Price is the largest text on every flyer; phone readable at ~350px thumbnail size.

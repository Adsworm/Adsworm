# Production Spec: Double-Sided LED Standee, 2 × 4 ft (610 × 1219 mm), Portrait, Outdoor

> **RECOMMENDED BUILD**
> **Primary:** double-sided aluminium-profile light box, 100–125 mm deep, powder-coated, hinged faces. Each face, outside to inside: 2 mm clear UV-stabilised polycarbonate, then backlit PET film (175–200 µm, 2× density), then 3 mm opal acrylic. A 3 mm white ACP centre divider carries 12 V lensed modules on both sides (4000 K, CRI ≥80, IP65+). One rain-proof SMPS per face, photocell + timer, 30 mA RCCB, gaskets, drain holes, ballasted MS base. **Est. ₹14,000–25,000.**
> **Budget:** double-sided "LED glow sign" (aluminium/GI frame, 440–510 gsm backlit flex, Konica solvent in backlit mode, same LEDs). **Est. ₹6,000–11,000.**
> INR figures are listing-based estimates, ex-GST/installation; usually billed on both faces (16 sq ft).

## 1. Constructions

| Build | Delhi listings | Verdict |
|---|---|---|
| Glow-sign frame + backlit flex | box ₹250–450/sq ft; print ₹25–55/sq ft ([src](https://sacreativestore.lovable.app/services/flex-printing-signage/delhi)) | **Budget.** Weave visible within 1 m; sags over time |
| Aluminium profile + film + opal acrylic | ₹280–600/sq ft ([src](https://m.indiamart.com/impcat/backlit-display.html)) | **Primary.** Rigid, smooth, sealable |
| Clip-on/snap frame, edge-lit LGP | ₹230–400/sq ft ([src](https://m.indiamart.com/impcat/clip-on-board.html)) | Dim at 2×4, not sealed. Indoor |
| SEG fabric | ₹345–700/sq ft ([src](https://m.indiamart.com/impcat/light-boxes.html)) | Indoor-rated ([src](https://floorstands.com/products/freestanding-led-light-boxes-36-x-48-seg-tension-fabric-frames-double-sided)); dust and monsoon rule it out |

**Centre divider is mandatory:** it prevents face-to-face light bleed, a known double-sided problem ([src](https://data.epo.org/publication-server/rest/v1.2/patents/EP1467336NWA2/document.html)), and daytime show-through.

## 2. Substrates

- **Star/frontlit flex:** opaque. Never use it in a light box.
- **Backlit flex (13–15 oz):** acceptable. Needs 2× ink; the scrim shows at night.
- **Backlit PET film on opal acrylic:** richest blacks, cleanest glow. **Pick this.**
- **Translucent vinyl on opal:** the thin ink film limits density, so darks go grey-green.
- **Direct UV on acrylic (CMYK-W-CMYK):** equal to film and more durable. Required for §7.

Single-density darks glow grey-green at night; use 2× density and/or the §7 mask.

## 3. Print settings and resolution

- **Printers:**
  - Flex: Konica KM512i solvent, 1440 dpi claimed ([src](https://www.textileinfomedia.com/product/konica-flex-printer-ye8)), about 720 dpi in production (unverified).
  - Film: eco-solvent Roland/Mimaki, 720×1440, ≥8 pass.
  - Acrylic/day-night: UV with white.
- **Backlit mode:** 2-pass overprint/double-strike or a "backlit" profile. It looks too dark unlit and right when lit ([src](https://www.signs101.com/threads/printing-backlit-panels.121187)).
- **Resolution:** min PPI = 3438 ÷ viewing inches ([src](https://irisshop.pixfizz.com/site/blog/Mastering-Resolution-for-Large-Format-Printing)). That is 87 ppi at 1 m and 175 ppi at 0.5 m, so **150 ppi at 1:1 is enough for 1–5 m.** Use 200 ppi for the face if the source supports it.
- **Pixel size at 630 × 1239 mm with bleed:** 3,721 × 7,317 px at 150 ppi; 4,961 × 9,756 px at 200 ppi.

## 4. Colour

- **Send CMYK, Coated FOGRA39**, unless the vendor supplies a media/mode ICC. Delhi RIPs often run unmanaged, so RGB converts unpredictably (unverified). Keep an RGB master for UV shops.
- **How colours shift:**
  - Deep greens go olive or muddy.
  - Screen-cyan is out of gamut.
  - Gold becomes ochre, and greenish under 6500 K.
  - Cream bleaches toward white when backlit.
- **Starting builds (confirm by strip test):**
  - Cyan line: **C100 M0 Y0 K0**. Core ≥3 mm with a 10–15 mm soft glow.
  - Gold: **C0–5 M25–35 Y70–85 K0–10**. No cyan.
  - Cream: **C0 M4–6 Y15–20 K0**.
  - Background, test three builds:
    - A: C85 M45 Y75 K70 (275%)
    - B: C80 M35 Y70 K55 (240%)
    - C: C75 M30 Y65 K40 (210%)
- B should read near-black with faint green glow at 2× (estimate). No K-only or 400% black: 240% rich black ([src](https://v2.4over4.com/guide/cmyk-values-for-print-explained)) is about 480% effective at 2×, risking pooling.

## 5. Bleed, safe area, wrap

- **Frame lip:** usually 15–25 mm per side (unverified; get the drawing). One snap-frame maker requires a ≥10 mm border ([src](https://printers.prontaprint.com/product/led-snap-frames/)).
- **Supply:** 610 × 1219 mm + **10 mm bleed** = **630 × 1239 mm**.
- **Safe area:** **40 mm inset** (530 × 1139 mm) for text, logo and QR. Face features ≥60 mm from the edge.
- **Budget flex wraps the frame:** add a **75 mm background extension per side** (760 × 1369 mm).

## 6. LEDs

- **Back-lit, not edge-lit:** LGP suits ≤50 mm boxes; perimeter strip leaves a 610 mm face's centre dim.
- **Module:** 12 V, 3× SMD2835 injection module, 160–175° lens, 0.72–1.5 W, IP65–67.
- **Spacing:** use a 2:1 spacing-to-depth ratio for 160–175° lenses ([src](https://www.power-supplies-australia.com.au/blog/led-modules-understanding-right-led-module-for-right-led-sign-installation)).
  - About 55 mm throw gives a **90–110 mm grid**, with the edge row ≤50 mm from the frame.
  - That is about 55–75 modules per face.
  - Each extra 51 mm of depth costs about 25% efficiency ([src](https://www.signmedia.ca/?p=9449)).
- **CCT: 4000 K** (or 5000 K), CRI ≥80. This range suits mixed warm and cool colours best ([src](https://graphics-pro.com/feature/led-insights-color-temperature-vs-color-rendering-index-which-is-better/)). The 6500 K default greys cream and greens gold. One bin for both faces.
- **Brightness:** UK ILE TR5 sets ≤800–1000 cd/m² for urban zones and central-area max:min ≤1.5:1 ([src](https://camdocs.camden.gov.uk/CMWebDrawer/Record/2801761/file/document)). I found no Indian standard. Field test: no LED dots visible through a blank face at 1 m. Fit a PWM dimmer.
- **Power:** about 100–220 W total. Use one rain-proof 12 V SMPS per face at ≤80% load. Add a dusk photocell, a timer (off at 23:00), a 30 mA RCCB, 1.5 mm² 3-core cable through a gland, and an earthed frame.

## 7. Day/Night and 3D

**Day/night is real and available.** UV printers lay colour-white-colour ([src](https://india.mimaki.com/product/inkjet/i-roll/ujv55-320/feature.html)), and Indian demand is reported ([src](https://indianprinterpublisher.com/blog/2023/03/monotech-showcases-uv)). Camera registration holds ≤2 mm ([src](https://lkc.hp.com/applications/double-sided-printing-block-out-or-day-night)); manual registration is about 3 mm.

- **Caveat:** a hidden image under a dark day-layer cannot show ([src](https://graphics-pro.com/education/how-to-create-backlit-signage-with-uv-printing/)).
- **Use a reverse blockout mask instead:** print opaque on the back everywhere except the face, text, gold and scan line ([src](https://www.printweek.in/news/wide-format-printer-2016-printech-digital-imaging-22400?amp=1)).
  - Spread openings 2–3 mm; open the scan line as a 10–15 mm band.
  - Result: green by day, jet-black surround and crisp glow at night.
- **Cost:** UV backlit is listed at ₹90/sq ft in Delhi ([src](https://m.indiamart.com/uvprinting-services/profile.html)). With white ink and layers, estimate ₹150–300/sq ft, about **+₹2,500–5,000** for both faces.
- **Risk:** misregistration halo; white-ink UV shops only; +2–4 days.

| Upgrade | Feasibility | Est. ₹/face |
|---|---|---|
| Raised acrylic letters, about 30 in of 3-in letters (lit ₹45–500/in, [src](https://dir.indiamart.com/delhi/acrylic-letter.html)) | Good. Keep the print under the letters dark; through-bolt and seal | 2,000–6,000 |
| 12 V silicone neon flex on the scan line, IP65+ (₹40–230/m, [src](https://m.indiamart.com/impcat/led-neon-light.html)), in a channel | Good. Print a 10–15 mm band to hide ±3 mm mounting error | 800–2,000 |
| Laser-cut layered acrylic border/logo, edge-lit | Moderate. Dust collects between layers | 2,500–6,000 |

## 8. Pre-press checklist (vendor confirms in writing)

1. Drawing: outer size, visible area, face cut size, lip, depth.
2. Named printer, media, mode, ICC.
3. **Strip test:** A/B/C, gold, cream, cyan, skin on real media/mode, viewed in the real box lit and unlit.
4. Signed 1:1 crop proof of the face.
5. Print surface and mirroring confirmed.
6. Face A/B and which face is street-side.
7. Mask and neon registration within ±2 mm.
8. Blank-face LED test: no dots, matched CCT.
9. Solvent prints dried ≥24 h before sealing.
10. IP ratings, RCCB, earthing, timer set, 2-hour burn-in.
11. Base anchored or ballasted against wind.

## 9. Files

- Delhi shops are CorelDRAW-centric; font substitution is common ([src](https://knowledgebase.bison.co.in/view_article.php?id=2390)). Supply:
  - **PDF/X-4** at 1:1 with bleed and crops, **text outlined**.
  - **Flattened CMYK TIFF** per face at 1:1, LZW, no layers or alpha.
  - A JPG preview.
- CDR if demanded: X7, curves, embedded images (version unverified).
- **Outline fonts: yes.** Keep a live-text master.

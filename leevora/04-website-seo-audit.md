# leevoraaesthetics.com: SEO Audit + Keyword Map (v3)

_Crawled 10 Nov 2026: all 45 sitemap URLs. Each page was parsed for title, meta, H1, schema, word count, images and local terms. Keywords were cross-checked against Google India autocomplete (80 seeds in total)._

## Verdict
**Technically, this site is in the top 5% of Indian clinic websites.**
- Every page has a unique title and meta description.
- Every page carries MedicalClinic / MedicalProcedure / FAQPage / Breadcrumb schema.
- Every page has 1,300–4,600 words, a medical disclaimer and AI crawlers allowed.

**It loses on four things:**
1. It isn't indexed yet.
2. It uses the wrong word for the #1 service.
3. It shows zero prices.
4. Its content targets low-demand topics.

---

## 🔴 Critical (fix this week)

### 1. The site isn't visible in search yet
- A `site:leevoraaesthetics.com` search returns nothing.
- Google autocomplete for "leevora" auto-corrects to **"levomac"** (an antibiotic). Google doesn't know the brand as an entity yet.
- **Fix:**
  - Verify in Google Search Console → submit `sitemap-index.xml` → URL Inspection → "Request indexing" for these 10 pages: `/`, `/laser/`, `/hair/prp/`, `/hair/gfc/`, `/skin/hydra-facial/`, `/bridal/`, `/salon/`, `/visit-us/`, `/skin/pigmentation/`, `/body/fat-freezing/`.
  - Then import the site into Bing Webmaster Tools (that feeds ChatGPT and Copilot).

### 2. "Laser hair removal" appears 0 times on the laser page
- The site says "laser hair reduction" (medically accurate) everywhere. But people search "laser hair **removal**" far more.
- Both terms have demand: "laser hair reduction cost" and "laser hair reduction kya hota hai" exist too.
- **Fix: use both. Keep the accuracy, capture the search.**

| Element | Current | Change to |
|---|---|---|
| Title `/laser/` | Laser hair reduction in West Delhi · Leevora Aesthetics | **Laser hair removal in West Delhi · Leevora Aesthetics** |
| H1 `/laser/` | Laser hair reduction | **Laser hair removal (laser hair reduction)** |
| First paragraph | (none) | "Laser hair removal, more accurately called laser hair reduction, ..." |
| Meta `/laser/` | Laser hair reduction for women and men… | "Laser hair removal for women and men at Subhash Nagar metro, two stops from Rajouri Garden. A qualified doctor checks skin and hair first. The consultation has no fee." |
| Title `/laser/beard/` | Beard laser hair reduction, West Delhi | **Beard laser hair removal in West Delhi** |
| FAQ (add) | (none) | "Is laser hair removal permanent?" Answer honestly with "permanent hair *reduction*". That captures the "permanent laser hair removal in delhi" demand without overclaiming |

### 3. Zero ₹ on the entire site
- "Price" appears 10× in the FAQ, but no actual figure appears anywhere.
- Cost is the **#1 search modifier** in every cluster: laser hair removal cost in delhi, hydrafacial cost in delhi, prp hair treatment cost in delhi, gfc treatment cost in delhi, chemical peel cost in delhi, fat freezing cost in delhi, pre bridal packages in delhi **with price**, steam bath in delhi price.
- **Fix:** publish "from ₹X" ranges on each service page, plus one `/prices/` page.
- Premium brands that show prices signal confidence, and most competitors hide theirs.

### 4. Brand-name consistency
- The website schema uses `name: "Leevora Aesthetics"` with `alternateName: "Leevora Aesthetic Clinic"`.
- **The GBP name must be exactly "Leevora Aesthetics"** (whatever the signage says, but it must match the site).
- Captions batch 1 has been updated to match.

---

## 🟠 High

### 5. Schema gaps (homepage MedicalClinic node)
Missing fields: `geo`, `hasMap`, `priceRange`, `image`, and GBP / Practo / Justdial / Facebook in `sameAs` (only Instagram is there). Add:
```json
"geo": { "@type": "GeoCoordinates", "latitude": 00.00000, "longitude": 00.00000 },
"hasMap": "<your Google Maps share link from GBP>",
"priceRange": "₹₹₹",
"sameAs": [
  "https://www.instagram.com/leevoraaesthetics/",
  "<GBP maps URL>", "<Practo URL>", "<Justdial URL>", "<Facebook URL>"
]
```
Take the latitude/longitude from the GBP pin (5+ decimals). Don't estimate them.

### 6. Missing alt text on images
- About 72 images on every page have no `alt` attribute. The count is identical site-wide, so these are template images (header, footer or gallery).
- **Fix them once in the layout component:** descriptive alts like "Laser room at Leevora Aesthetics, Subhash Nagar".
- This also feeds Google Images for "skin clinic subhash nagar".

### 7. Keyword-weak H1s
- Homepage H1: "Your skin. Your pace." Keep it as the brand line, but make the **H1** "Skin clinic, laser and unisex salon at Subhash Nagar metro, West Delhi", with the brand line as the subtitle.
- `/hair/prp/` H1 "PRP for hair" → "PRP hair treatment for hair fall"
- `/hair/gfc/` H1 "GFC for hair" → "GFC hair treatment (growth factor concentrate)"

### 8. Rajouri Garden only appears in the metro directions
- Rajouri Garden is the demand hub. On money pages (laser, PRP, GFC, hydra facial, skin, salon), add one natural line: "At Subhash Nagar metro, two stops from Rajouri Garden and one from Tilak Nagar." Keep it factual, not stuffed.

---

## 🟡 Medium: New pages (demand proven, page missing)

| New URL | Target query (autocomplete-verified) |
|---|---|
| `/laser/full-body/` | full body laser hair removal cost delhi |
| `/laser/face/` | laser hair removal face (cost, women, how many sessions) |
| `/laser/underarm/` | underarm laser hair removal cost in delhi |
| `/laser/men/` | laser hair removal for men (price) |
| `/prices/` | all "cost in delhi" queries |
| `/journal/gfc-vs-prp/` | gfc vs prp which is better · gfc vs prp vs exosomes |
| `/journal/laser-hair-removal-side-effects/` | laser hair removal side effects · is it safe for face |
| `/journal/laser-hair-removal-cost-delhi/` | laser hair removal cost in delhi |
| `/journal/hydrafacial-cost-delhi/` | hydrafacial cost in delhi |
| `/journal/pre-bridal-packages-delhi/` | pre bridal packages in delhi with price |
| `/hi/prp-hair-treatment-kya-hota-hai/` | prp hair treatment kya hota hai (Hindi) |
| `/hi/laser-hair-reduction-kya-hota-hai/` | laser hair reduction kya hota hai (Hindi) |

The current journal (steam room, potli after gym, salon vs clinic facial) targets topics with little search demand. Keep those posts, but put the next 8 into the table above.

---

## Full keyword map (v3): matched to the site's real services

### Subhash Nagar level (strong local demand → GBP + homepage + /visit-us/ + /salon/)
skin clinic subhash nagar · skin doctor / skin specialist subhash nagar · dermatologist subhash nagar · **salon subhash nagar · unisex salon subhash nagar · hair salon subhash nagar · parlour subhash nagar** · spa subhash nagar · **spa near subhash nagar metro station**

### Rajouri Garden level (demand hub → GBP posts + service-page proximity line)
laser hair removal rajouri garden · skin clinic rajouri garden · aesthetic clinic rajouri garden · hair clinic / hair treatment rajouri garden · hydra facial rajouri garden · facial in rajouri garden · hair spa rajouri garden · hair salon rajouri garden · spa / massage rajouri garden · weight loss clinic in rajouri garden

### West Delhi level
laser hair removal west delhi · hydrafacial in west delhi · aesthetic clinic in west delhi · best skin clinic in west delhi

### Delhi level (website service pages + journal)
laser hair removal in delhi (cost) · prp hair treatment in delhi · gfc treatment in delhi · hydrafacial in delhi (cost) · chemical peel in delhi · pigmentation treatment in delhi · acne / acne scar treatment in delhi · fat freezing / cryolipolysis in delhi · wart / skin tag removal in delhi · pre bridal packages in delhi · potli massage in delhi · steam bath in delhi

### Failed (no demand; don't target)
laser hair removal subhash nagar · prp/gfc + subhash nagar/rajouri · pigmentation/acne treatment rajouri · facial subhash nagar · weight loss clinic west delhi · skin clinic near pacific mall

---

## GBP category decision (the site is clinic + salon + spa)
- **Primary:** Skin care clinic. It's the money service, and the site schema is MedicalClinic.
- **Secondary:** Laser hair removal service · Hair salon · Beauty salon · Day spa · Facial spa · Massage spa · Weight loss service.
- **Trade-off:** salon queries ("salon subhash nagar") will rank weaker under a clinic primary category.
  - A separate salon GBP is only allowed if the salon runs as a distinct business (its own signage, entrance and phone).
  - Otherwise it risks suspension. Don't do it on the same listing.

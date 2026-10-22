# 02 Concepts + scripts (Thu 22 Oct 2026, both post today on @adsworm)

Reel 05 format. Drafts: `reel-A.draft.json`, `reel-B.draft.json` (121 words each, about 45 s, no line over 14 words).

**Pick check:** I kept #2. It quotes Meta's own notice word for word, and two outlets reported it independently. The reel says "Meta has told advertisers" and a card flags that there is no Help Center page yet. The advice ("decide before the 28th") stays safe even if details change. #3 rests on secondhand Redseer coverage and would make a second festive reel.

---

## Reel A: "Why your ads feel expensive this October"

**Concept.** October feels "down": same budget, fewer sales. We name the cause, a pricier festive auction, then turn it around. In the same data, cost per sale *fell* because buyers were ready. So don't cut spend; fix what happens after the click. Calm, no panic.

**Target viewer:** D2C, clinic, local-service and coach owners running Meta ads who saw costs creep up this month.

**Hooks:** (1) "Meta says its average price per ad is up twelve percent on last year." **← pick:** an official number that a non-marketer gets at once. (2) "Last Black Friday, ad prices ran 84% above September." (3) "Diwali is {days} days away, and your ads just got pricier."

| Who | Line | Card |
|---|---|---|
| AMAN | Meta says its average price per ad is up twelve percent on last year. | big +12% · receipt "Meta Q2 2026 · Meta's own number" |
| RIYA | So that's why October feels slow? Same budget, fewer sales? | |
| AMAN | Partly. Here's what's going on before Diwali. | big {days} days to Diwali · date chips 6/8/27 Nov |
| AMAN | CPM, the price of a thousand views, climbs into Black Friday. | ① big "CPM = price of 1,000 views" · chip "2024: climb began mid-Oct" |
| AMAN | Last year, Black Friday CPM was eighty-four percent above September. | bars BF week +59%, BF day +84% · receipt Lebesgue |
| RIYA | So should I pause my ads till Diwali? | |
| AMAN | No. In that same data, cost per sale fell twenty percent. | ② big −20% cost per sale |
| AMAN | Because conversion rate, the share who buy, rose forty-eight percent. | bar +48% · note "Ads cost more. More people ready to buy." |
| RIYA | So what do I actually fix? | |
| AMAN | Don't cut spend. Fix what happens after the click. | ③ compare ✕ Cut spend / ✓ Fix after the click |
| AMAN | Sharper offer, faster page, easier checkout. That's where money leaks. | steps 1-2-3 |
| AMAN | Comment OCTOBER and we'll check where your ad money is leaking. | comment UI typing OCTOBER |
| RIYA | Doing that before Diwali! | checklist unlocks: offer / page / checkout / tracking |

**CTA:** comment **OCTOBER**. **What we send:** a free pre-Diwali leak check: their top 3 leaks (offer, page, checkout, tracking) with a fix for each, by DM. No result promised.

**Sources:** Meta Q2 2026 results (investor.atmeta.com, +12%). Lebesgue, 16 Oct 2026 (CPM +59%/+84%, cost per purchase −20%, conversion rate +48%, 2024 climb from mid-October; card says "mostly US brands"). Not used: Razorpay 25–40% (unsourced), any India CPM percentage.

---

## Reel B: "Meta changes your live ads on 28 October"

**Concept.** A real deadline 6 days away. Meta has told advertisers it will switch on "product browsing" in running ads, so a tap may open an in-app product page before the website. We explain the change, label +3% as Meta's own number (metric undefined), and leave a simple choice: keep it, opt out, or test it on a few ads. Helpful, not scary.

**Target viewer:** D2C and e-commerce owners running Meta sales ads to their own website. These are the owners who care where the click lands and how sales are tracked.

**Hooks:** (1) "On October twenty-eighth, Meta will change ads you're already running." **← pick:** a hard date plus "your ads", stake first. (2) "You have {days} days to decide about this Meta change." (3) "Meta's adding a shop page to your ads unless you opt out."

| Who | Line | Card |
|---|---|---|
| AMAN | On October twenty-eighth, Meta will change ads you're already running. | big 28 OCT · chip "{days} days left to decide" |
| RIYA | Wait, without asking me? Changes what? | |
| AMAN | Meta has told advertisers. Here's what changes, and your choice. | browser ppc.land headline, 15 Oct |
| AMAN | Meta's notice says it will add product browsing to existing ads. | ① quote of the notice · receipt |
| AMAN | So a tap may open a product page inside the app first. | phone mock · chips Tap → Product page in app → Your website |
| RIYA | Before my website? Is that good or bad? | |
| AMAN | Meta says its test showed three percent more conversions, on average. | ② big +3% · receipt "Meta's own number · 6–21 Aug · ~117,700 advertisers" |
| AMAN | That's Meta's own number. It didn't say which conversions. | note · chip "no Help Center page yet" |
| RIYA | So what should I do? | |
| AMAN | Before the twenty-eighth, decide. Opt out from Meta's notice, or ad by ad. | ③ steps: find notice / opt out all / per ad (Advantage+ creative) |
| AMAN | If your website does the selling, test it on a few ads. | steps: keep on a few / opt out rest / compare sales |
| AMAN | Not sure? Comment BROWSE and we'll check your account for free. | comment UI typing BROWSE |
| RIYA | Checking mine today! | checklist unlocks: which ads / keep or opt out / how to switch off |

**CTA:** comment **BROWSE**. **What we send:** a free account check: which live ads it touches, keep or opt out for their setup, and a screenshot guide to switching it off per ad.

**Sources:** Meta's advertiser notice via ppc.land (15 Oct 2026) and relevantaudience.com (quote, 28 Oct date, +3% from the 6–21 Aug test across ~117,700 advertisers, opt-out routes). On-screen caveat: no Help Center page.

---

**Render notes:** `{days}` (cards only, never spoken) uses `vars.countdown`: A → 2026-11-08, B → 2026-10-28. `voice.py` ignores the extra `title` key. 28 Oct is a Wednesday, so the script never names a weekday.

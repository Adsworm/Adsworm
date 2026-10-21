---
name: creative-performance-loop
description: Reads Meta results per ad (hook rate, hold rate, CTR, CPA), maps them to hook/offer/CTA via ad names, writes the next variant matrix. Read-only. Use for "what's working".
---

# Creative Performance Loop

Creative is the biggest lever left in Meta's automated delivery. This skill turns spend into the next brief.

## 1. Pull the data (read-only)

- **Meta MCP:** use `ads_get_ad_entities` and the insights tools for ad-level metrics. Use `ads_insights_performance_trend` for fatigue.
- **Adspirer** (alternative): `analyze_meta_ad_performance`, `detect_meta_creative_fatigue`.
- **Window:** the last 7 days for decisions and the last 28 days for patterns.
- **Pull per ad:** impressions, spend, 3-s video plays, ThruPlays, link CTR, CPA or ROAS, frequency.

Never pause, scale, edit or upload without the user saying so explicitly in this conversation. Anything you would change goes into a recommendation instead.

## 2. Compute

| Metric | Formula | Reads as |
|---|---|---|
| Hook rate | 3-s video plays ÷ impressions | Did the first frame and the first 2 s stop the thumb? |
| Hold rate | ThruPlays ÷ 3-s plays | Did the middle earn attention? |
| CTR (link) | link clicks ÷ impressions | Did offer and CTA convert attention to intent? |
| CPA / ROAS | spend ÷ results, revenue ÷ spend | The only number the client pays for |

Judge against **this account's median**, not internet benchmarks. Accounts, verticals and placements differ too much.

**Evidence floor before calling anything:**
- About 1,000 impressions to judge hook rate.
- Spend of at least 1–2× target CPA to judge CPA.
- Below that, label it "insufficient data".

## 3. Map results back to creative

Parse the ad name `CAMPAIGN_H#-O#-C#_FORMAT_vN` (from `ad-variant-matrix`). Aggregate by each axis to separate effects:
- Which **hook** wins on hook rate across offers?
- Which **offer** wins on CTR and CPA across hooks?
- Does **9:16 vs 4:5** change the winner?

Ads not named to the convention: tag them manually (hook angle, offer, format, first-frame type) before aggregating.

## 4. Decide

- **Winner:** best CPA/ROAS with the evidence floor met. Recommend scaling the budget gradually.
- **Fatigue:** CTR or hook rate falling about 20%+ over 7 days while frequency rises. Brief a refresh of the same angle with a new first frame.
- **Loser:** bottom quartile on the primary KPI with the floor met. Recommend pausing.
- **Learning:** state one sentence per axis, e.g. "Pain-angle hooks beat outcome hooks on hook rate by about 30% in both formats."

## 5. Write the next round

Output `props/matrix.next.json` for `ad-variant-matrix`:
- Keep the winning axis values.
- Add 2–3 new values on the **weakest** axis.
- Keep IDs stable (a winner stays H2) and give new ideas new IDs (H4, H5).

Add a short `insights.md`:
1. The table per axis.
2. Winners, fatigue and losers, each with numbers.
3. What changes next round, and why.
4. Recommended account actions, awaiting approval.

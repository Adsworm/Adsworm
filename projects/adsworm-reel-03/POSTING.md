# DIWALI · 17 DIN — posting kit (reel 03, v2 after creative-director review)

## Files
- `out/DIWALI-17-DIN_9x16.mp4` — 59 s, 1080×1920, H.264 + AAC, −14 LUFS.
- `out/cover.png` — frame 0: "17 DIN", the three locked updates and the hook caption. Use it as the cover.

## The day count is live
"17 din" is true on **22 Oct 2026** only. The pipeline computes days-to-Diwali from today's date (`vars.countdown` in `script/script.json`), so to post on another day re-render once: `npm run render` (about 3 minutes). The hook line's voice, caption and card number all update together. `REEL_DAYS=16 npm run render` forces a number. Change the caption's first line to match.

## Before posting (owner)
1. **Confirm the on-screen facts once** against `script/sources.md` (official Meta pages and Criteo via Social Samosa; dates 6–19 Oct 2026).
2. **Build the lead magnet:** a 1-page "Diwali Meta Ads Checklist" PDF with the 7 links from `sources.md`.
3. **Wire the keyword:** comment **DIWALI** → auto-DM with the PDF (ManyChat, or Meta Business Suite's free comment automation, max 5 keywords). Test it from a second account before posting.
4. **Trial Reel first** (non-followers only) to read the 3-second skip rate and the retention curve on the hook; then publish.
5. Reply to every comment in the first hour. Comments are a ranking signal.

## Caption
> Diwali mein 17 din. Meta ne chupchaap 3 cheezein badal di — aur teeno aapka paisa bachaati hain.
>
> ① Advantage+ ab ek static image se video bana deta hai — live in Ads Manager (6 Oct)
> ② Naya ad model GEM: +18.9% conversions — par same creative ke variations ko kam reward (13/19 Oct)
> ③ WhatsApp: 1 Oct se service messages charged (1,000 free/month) — par ad se aaye customer ko reply ke baad 7 din free
> Bonus: pichhli Diwali India mein digital ad costs CPM +26%, CPC +45% (Criteo). Creative 6 Nov Dhanteras se pehle ready rakho.
>
> Comment **DIWALI** — poori checklist + official links DM mein. Save karo, partner ko bhejo.
>
> #metaads #diwali2026 #d2cindia #clinicmarketing #performancemarketing #adsworm

Pinned comment: "Sources: Meta for Business (6 Oct, 19 Oct), engineering.fb.com (13 Oct), WhatsApp pricing page, Criteo India via Social Samosa. Comment DIWALI for the PDF."

## Judge it by
Skip rate (3 s), retention-curve flatness, sends per reach, comments. Not likes. Compare against the account's last 5 reels.

## Paid use (after 24–48 h organic)
- **Boosting the organic post** keeps the comment CTA. Fine for an engagement boost: ad account **Adsworm** (231260619687022) · Page Adsworm · IG @adsworm, ₹1,000/day × 7 days, created paused, activated only on the owner's go.
- **A messages/leads campaign** should use the paid variant instead: `npm run render -- --paid` → `out/REEL-03_PAID_9x16.mp4`. The end card becomes a plain "DM DIWALI" card (no Instagram comment UI) and the spoken CTA line changes with it. Upload it as a new ad creative; do not boost the organic post with it.

## Next episodes in this module (same pipeline: edit `script/script.json`, run `npm run render`)
1. "₹40,000 ka ad budget, 0 patients — ye 3 galtiyan" (clinic owners; Ads Manager receipts from a real account, anonymised)
2. "Meta ne 28 Oct se product browsing on kar diya — aapke ads mein" (if the notice appears in your account: screenshot it as the receipt)
3. "Diwali ke baad CPM gir jaata hai — Nov–Feb shaadi season ka plan" (Meta India festive guidance)

# The Diwali Spike (20 Nov 2026)

A 1:31 landscape film for LinkedIn, YouTube, the website and pitches. English narration. One board: a four-bar chart of the cost of one enquiry, four detail clusters under it, an end slate.

## Sources

Every number is listed in `script.json` under `fact_notes`. The only data source is `docs/pipeline/2026-11-12/02-account-data.md`: 18 Meta ad accounts, read on 12 Nov 2026, anonymised. No client or account name appears in the film or in this folder.

## What the film does not claim

- That ad prices rose. In October they were about 5% lower than in September (median account).
- That the festive sales caused the rise. Line 12 calls it "our reading" and the card says "not a measured cause".
- That costs are back to normal. The three days after Diwali are about October's level, still about 12% above September, and the film says three days can reverse.
- Anything about ad prices in Diwali week. The close is limited to October: no Diwali-week click cost was measured.
- "Enquiry" is a chat started from an ad. It is not a booking. The screen says so twice.

## Checks done

- **Facts and clarity:** an independent reviewer read the script against the data file on 20 Nov 2026. Verdict: approve with fixes. All eight fixes were applied (period and scope on seven lines, "a smaller share", the opening question).
- **Voice:** Kokoro `am_michael` (open-source, Apache-2.0). Higgsfield had 0.45 credits and this narration needs about 5.5. Transcript check: all 210 script words were heard correctly ("enquiry" is written "inquiry" by the recogniser; same sound). `split_takes.py` flagged no line. Tone and accent were not judged by ear: this check cannot hear.
- **Picture:** one still per line was looked at after each change (three rounds). The hero of each line sits clear of the caption band.

## To change the voice

Save one take per section in `audio/takes/`, run `split_takes.py`, then `build_narration.py --tail 7.5`. The scene re-times itself; re-run the sound and the render (see `../README.md`).

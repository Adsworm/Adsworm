"""Retention QA from the timeline (rules: docs/playbook/EDITING-PSYCHOLOGY.md §6).

    python3 scripts/qa_report.py          # after voice.py; prints PASS / WARN per check

Checks what can be measured without watching: pacing of on-screen changes, speaker holds, reactions,
caption chunks, payoff position, CTA time on screen, script length. It also catches cue typos: any
`word` cue that is never spoken is listed, because that element would silently never appear.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tl = json.loads((ROOT / "src/reel/timeline.json").read_text())
FPS = tl["fps"]
dur = tl["durationInFrames"] / FPS
lines, sections, beats = tl["lines"], tl["sections"], tl["beats"]
norm = lambda w: re.sub(r"[^a-z0-9%]", "", w.lower())
problems, out = [], []


def check(ok, label, detail=""):
    out.append(f"  {'PASS' if ok else 'WARN'}  {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        problems.append(label)


# ---- every moment something changes on screen -------------------------------------------------
changes, missing = [], []
for sec in sections:
    # cue words = spoken words + caption tokens (Hinglish cues are written against the Latin caption);
    # a word and its identical caption token count once, as in Reel.tsx
    merged = sorted([w for l in lines if l["section"] == sec["id"] for w in l["words"] + [{"t": k["t"], "w": k["w"]} for k in l["tokens"]]], key=lambda w: w["t"])
    words = []
    for w in merged:
        if not any(norm(y["w"]) == norm(w["w"]) and abs(y["t"] - w["t"]) < 0.02 for y in words[-3:]):
            words.append(w)

    def word_t(cue, after):
        w0, _, nth = cue.partition("#")
        hits = [w["t"] for w in words if w["t"] >= after - 0.05 and norm(w["w"]).startswith(norm(w0))]
        i = (int(nth) if nth else 1) - 1
        if i >= len(hits):
            missing.append(f"{sec['id']}: \"{cue}\"")
            return None
        return hits[i]

    def cue_t(word, at, after, fallback):
        if word:
            return word_t(word, after)
        if at:
            return beats.get(at, 0) / FPS if at in beats else None
        return fallback

    changes.append(sec["start"] - 0.2)  # whip
    for v in sec.get("views", []):
        vs = beats.get(v["at"], 0) / FPS
        if v.get("word"):
            vs = word_t(v["word"], vs) or vs
        changes.append(vs)
        for it in v["items"]:
            t0 = cue_t(it.get("word"), it.get("at"), vs, vs)
            if t0 is None:
                continue
            changes.append(t0)
            for key, wk, ak in (("actors", "word", "at"), ("msgs", "word", "at"), ("lines", "word", "at"), ("rows", "word", "at")):
                for sub in it.get(key, []) if isinstance(it.get(key), list) else []:
                    if not isinstance(sub, dict):
                        continue
                    for w_key, a_key in ((wk, ak), ("outWord", "outAt"), ("sayWord", "sayAt"), ("badgeWord", "badgeAt"), ("verdictWord", "verdictAt")):
                        if sub.get(w_key) or sub.get(a_key):
                            t1 = cue_t(sub.get(w_key), sub.get(a_key), vs, None)
                            if t1 is not None:
                                changes.append(t1)
                    for seg in sub.get("segs", []):
                        if seg.get("word") or seg.get("at"):
                            t2 = cue_t(seg.get("word"), seg.get("at"), vs, None)
                            if t2 is not None:
                                changes.append(t2)
            for c in it.get("items", []) if it["type"] == "checks" else []:
                t3 = word_t(c["word"], vs)
                if t3 is not None:
                    changes.append(t3)
            for k in ("adWord", "emojiWord", "statusWord", "smileWord", "tapWord", "webWord", "goodWord"):
                if it.get(k):
                    t4 = word_t(it[k], vs)
                    if t4 is not None:
                        changes.append(t4)
reactions = []
for i, l in enumerate(lines):
    if i == 0 or lines[i - 1]["who"] != l["who"]:
        changes.append(l["start"])  # speaker swap
    if l.get("react"):
        w = next((x["t"] for x in l["words"] + l["tokens"] if l.get("reactWord") and norm(x["w"]).startswith(norm(l["reactWord"]))), l["start"])
        reactions.append(w)
        changes.append(w)
    if l.get("pre"):
        reactions.append(l["start"] - 0.2)
    pills = [t["t"] for i, t in enumerate(l["tokens"]) if t["pill"] and not (i and l["tokens"][i - 1]["pill"])]
    if pills:
        changes.append(pills[-1])  # the board's punch-in on the line's last highlighted phrase
changes.append(0.0)  # frame 0: the push-in on a finished hook board
changes = sorted(set(round(c, 2) for c in changes if 0 <= c <= dur))

# ---- checks -----------------------------------------------------------------------------------
words_total = sum(len(l["words"]) for l in lines)
spoken_end = lines[-1]["end"]
check(lines[0]["start"] * FPS <= 6, "first spoken word by frame 6", f"frame {lines[0]['start'] * FPS:.0f}")
check(sum(1 for c in changes if c <= 3.0) >= 3, "≥ 3 on-screen changes in the first 3 s", f"{sum(1 for c in changes if c <= 3.0)}")
gaps = [(b - a, a) for a, b in zip(changes, changes[1:] + [spoken_end])]
g, at = max(gaps)
check(g <= 4.0, "max gap between on-screen changes ≤ 4 s", f"{g:.1f}s at {at:.1f}s")
busy = max(sum(1 for c in changes if s <= c < s + 2) for s in [x / 2 for x in range(int(dur * 2))])
check(busy <= 5, "never more than ~2 changes/s for 2 s", f"busiest 2 s has {busy}")
holds, start = [], lines[0]["start"]
for a, b in zip(lines, lines[1:]):
    if a["who"] != b["who"]:
        holds.append((b["start"] - start, start, a["who"]))
        start = b["start"]
holds.append((spoken_end - start, start, lines[-1]["who"]))
long = [(h, s, w) for h, s, w in holds if h > 6 and not any(s < r < s + h for r in reactions)]
check(not long, "no speaker holds > 6 s without a swap or reaction", ", ".join(f"{w} {h:.1f}s at {s:.1f}s" for h, s, w in long))
check(len(reactions) >= 4, "≥ 4 reactions (listener faces / pre-line beats)", str(len(reactions)))


def chunks(tokens):
    res, cur = [], []
    txt = lambda c: " ".join(x["w"] for x in c)
    for tok in tokens:
        if cur and (len(cur) >= 4 or len(txt(cur + [tok])) > 20):
            res.append(cur)
            cur = []
        cur.append(tok)
        if re.search(r"[.!?,…:]$", tok["w"]) and len(cur) >= 2:
            res.append(cur)
            cur = []
    if cur:
        if res and len(cur) == 1 and len(txt(res[-1] + cur)) <= 22:
            res[-1] += cur
        else:
            res.append(cur)
    return res


fast, short = [], []
for l, after in zip(lines, lines[1:] + [None]):
    cs = chunks(l["tokens"])
    for c, nxt in zip(cs, cs[1:] + [None]):
        # a line's last chunk stays in the bubble until the next line starts
        end = nxt[0]["t"] if nxt else (after["start"] if after else dur)
        d = max(0.05, end - c[0]["t"])
        text = " ".join(x["w"] for x in c)
        if len(text) / d > 22:
            fast.append(f"\"{text}\" {len(text) / d:.0f} ch/s")
        if d < 0.4:
            short.append(f"\"{text}\" {d:.2f}s")
check(not fast, "caption chunks ≤ ~20 characters/s", "; ".join(fast[:4]))
check(len(short) <= 2, "caption chunks stay ≥ 0.4 s", "; ".join(short[:4]))
if tl.get("payoff"):
    p = tl["payoff"]["frame"] / FPS / spoken_end
    check(0.5 <= p <= 0.75, "payoff lands at 55–70% of the runtime", f"{p * 100:.0f}%")
else:
    check(False, "payoff defined (riser → breath → hit)")
cta = next((beats[v["at"]] / FPS for s in sections for v in s.get("views", []) if any(i["type"] == "comment" for i in v["items"])), None)
nxt = next((beats[v["at"]] / FPS for s in sections for v in s.get("views", []) if any(i["type"] == "follow" for i in v["items"])), dur)
check(cta is not None and nxt - cta >= 2, "CTA keyword on screen ≥ 2 s", f"{(nxt - cta) if cta else 0:.1f}s")
# Hindi carries short particles (में, ने, के, है) that English does not, so the same runtime holds more words.
lo, hi = (95, 120) if tl.get("lang", "en") == "en" else (110, 140)
check(lo <= words_total <= hi, f"{lo}–{hi} spoken words", str(words_total))
check(dur <= 55, "runtime ≤ 55 s", f"{dur:.1f}s")
check(max(len(l["words"]) for l in lines) <= 14, "no line over 14 words", str(max(len(l["words"]) for l in lines)))
check(not missing, "every word cue is actually spoken", "; ".join(missing))
if tl.get("lang", "en") != "en":
    # Hinglish: `say` is Devanagari + English, `show` is its Latin caption. Same word count per line
    # means every caption word lights up on its own spoken word.
    uneven = [f"l{l['n']} say {len(l['words'])} / show {len(l['tokens'])}" for l in lines if len(l["words"]) != len(l["tokens"])]
    check(not uneven, "caption has one word per spoken word (Hinglish)", "; ".join(uneven))

print(f"QA · {dur:.1f}s · {words_total} words · {len(changes)} on-screen changes (one every {spoken_end / max(1, len(changes)):.1f}s) · {len(reactions)} reactions")
print("\n".join(out))
sys.exit(1 if missing else 0)

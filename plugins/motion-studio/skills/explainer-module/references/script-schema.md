# script.json schema (engine v4)

One file drives voice, captions, acting, board and sound. Source of truth for the types: `src/reel/views.tsx` (`Item`), `src/reel/Reel.tsx` (`Timeline`).

```jsonc
{
  "voices": {"AMAN": {"voice_type": "preset", "voice_id": "…"}, "RIYA": {"voice_type": "preset", "voice_id": "…"}},
  "direction": "One paragraph: who they are, the energy, how they talk.",   // ElevenLabs prompt
  "gapCap": 0.22, "tempo": 1.05, "leadInMs": 60, "tailMs": 1500, "bedGain": 0.07,
  "vars": {"countdown": {"to": "2026-11-27"}},            // optional → {days} in any board text
  "brand": {"names": {"AMAN": "AMAN · ADSWORM", "RIYA": "RIYA · SALON OWNER"}, "side": {"AMAN": "left", "RIYA": "right"}},
  "loop": {"text": "late? how?", "answer": "reply in 1 hour", "until": "l8"},   // chip pinned until the payoff (≤ 16 chars)
  "payoff": {"beat": "l8", "pauseMs": 350},               // held breath + riser + hit before this line
  "sections": [{
    "id": "hook", "label": "THE LEAD MYTH",               // pill, ≤ 18 chars
    "source": "small receipt line under the board",
    "lines": [{
      "who": "AMAN",
      "tags": "[excited]",                                // voice only
      "say": "Your leads aren't bad. You're just late.",  // spoken; numbers as words
      "show": "Your leads aren't bad. [You're just late.]", // caption; [pills] = stressed phrase
      "beat": "l1",                                       // unique id; views and cues point at it
      "react": "doubt", "reactWord": "late",              // the LISTENER's face, from that word
      "pre": "laugh"                                      // the SPEAKER's face in the beat before the line
    }],
    "views": [{"at": "l1", "word": "optional spoken word", "items": [ … ]}]
  }]
}
```

## Cues
- `at` = a beat id (the moment that line starts). `word` = a word spoken in this section at or after the view starts; matching is lower-case, letters/digits only, prefix match ("sale" also matches "salesman": use `"sale#2"` for the second hit).
- A view takes over the board at its cue; the first view of a section must start on the section's first beat (no `word`), or the board whips in empty.
- Inside an item, sub-elements have their own cues (`word`/`at`, `outWord`, `sayWord`, `badgeWord`, `verdictWord`, `adWord`, `emojiWord`, `statusWord`).
- `python3 scripts/qa_report.py` lists every word cue that is never spoken.
- Faces available: aman `laugh surprised wink`, riya `shock laugh doubt worry`.

## Board items
| type | use | key fields |
|---|---|---|
| `headline` | hook claim, 2–3 stacked lines | `lines[{text, tone?, word?}]`, `emoji`, `emojiWord` |
| `scene` | stage an analogy with actors | `actors[{emoji \| "SHOP", sign?, label?, x, y, size?, enter: pop\|left\|right\|drop, word/at, outWord, say, sayWord, badge, badgeWord, badgeTone}]` (stage 880×500) |
| `chatThread` | a DM thread; timestamps tell the story | `name`, `msgs[{from: them\|me, text, time?, word/at}]`, `status`, `statusWord/At`, `statusTone` |
| `aiChat` | an AI-assistant answer with a labelled sponsored card | `question`, `adWord`, `brand`, `adLine`, `note` |
| `clock` | time passing | `to`, `unit`, `label` |
| `plan` | plans against a deadline (bars turn red past it) | `from`, `to`, `deadline`, `deadlineLabel`, `rows[{label, start, word/at, segs[{len, text, word/at}], verdict, verdictWord}]` |
| `stat` | one hero number, counts up | `value`, `prefix`, `suffix`, `label`, `color`, `arrow` |
| `versus` | two numbers that seem to clash | `left`, `right`, `qAt` |
| `checks` | the fix as ticks on spoken words | `items[{text, word}]` |
| `compare` | ✕ what people do vs ✓ what works | `bad`, `good`, `goodWord` |
| `sticker` | tilted stamp = punctuation, a joke | `text`, `color`, `x`, `y`, `rotate`, `word/at` |
| `big`, `chip`, `chips`, `note`, `browser`, `receipt`, `bars`, `steps` | supporting pieces | see `views.tsx` |
| `comment`, `follow` | CTA: comment keyword UI, then follow flip + share line | `keyword` / `share` |

Tones: `red green blue gold pink ink`. Board content area ≈ 890 × 540 px; stickers use absolute `x, y` inside it.

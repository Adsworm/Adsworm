---
name: explainer-module
description: The voice-led Instagram explainer reel that holds retention — a teacher and a student as talking heads (lip-flap + facial reactions), karaoke bubble captions, a proof board that builds on the spoken word, sound played by the visuals, an open-loop chip held until a payoff. One script.json drives everything. Use for educational, news or "relatable mistake" reels for business owners; use instead of kinetic typography when the goal is watch time, sends and comments.
---

# Explainer Module (engine v4)

Template project: `projects/adsworm-reel-10` (copy the folder, replace `script/script.json`, generate the dialogue, render). Rules behind every choice: `docs/playbook/REEL-PLAYBOOK.md` (hooks, dialogue), `docs/playbook/EDITING-PSYCHOLOGY.md` (editing, sound, QA numbers), `docs/playbook/REFERENCE-Det2rTBzoEq.md` (the reference reel). Read `references/retention-rules.md` before writing a script and `references/script-schema.md` while writing it.

What failed before, so don't rebuild it: kinetic type on dark (reel 01), cinematic abstract (02), a floating orb and flying camera (04: "nobody understood it"), a polite stats lecture with full-body avatars (06–07: "no fun, feels manufactured").

## The format

| Layer | What it does | Rule |
|---|---|---|
| Two busts, bottom | AMAN teaches, RIYA is the viewer. Mouth frames follow voice loudness; the listener reacts (shock, laugh, doubt, worry) | The student says the wrong belief out loud, proposes the wrong move, the teacher cuts in. ≥ 4 reactions per reel |
| Karaoke bubble | 2–4 words at a time, active word lit, pills on the stressed phrase | ≤ 4 words and ≤ 20 characters per chunk; captions ≥ 56 px |
| Proof board, top | One section = one board. Views switch on a beat or a spoken word; items inside land on their own words | A change every 2–4 s, never > 2 per second. ≤ 7 readable words and one hero number per state. Show an object or a scene, not a word list |
| Open-loop chip | The question the hook raised stays pinned to the board; turns green at the payoff | Uncertain hook, certain payoff; payoff at 55–70% of the runtime |
| Sound | Each visual plays its own effect (`Sfx.tsx`); pad ducks under the voice; riser → 0.35 s breath → bass hit on the payoff | Effects ≥ 6 dB under the voice, each on a visual event, pitch varied |
| Frame 0 | A finished composition: hook headline readable, both faces in frame | First word by frame 6, hook claim (≤ 7 words) readable by frame 15 |

## Script rules (the part that decides if it works)

1. **Hook** = a contradiction or a "that's me" in ≤ 12 words, said by the teacher to the viewer. Not a topic, not a stat.
2. **The student is wrong out loud** ("I called them the very next morning!"), then proposes the wrong fix; the teacher interrupts. Never polite Q&A.
3. **One everyday analogy** staged on the board (a shop, a new salesman, a visiting card) instead of a definition.
4. **Max 2 numbers spoken**; other figures live on the board with a receipt chip (source, date, "Meta's own number", "US, 2011"…).
5. **95–115 spoken words, lines ≤ 12 words**, 40–50 s. One speaker never holds > 6 s without a swap or a reaction.
6. **CTA once**: "Comment KEYWORD" + exactly what arrives by DM. Then a share line that names a person ("send this to whoever answers your enquiries"), and a last line that echoes the hook.
7. **Facts only with receipts**: write them in `script/sources.md`; an independent approval pass verifies every spoken or shown claim before any voice credit is spent. Illustrative UI is labelled; no platform logos.

## Pipeline

```bash
cp -r projects/adsworm-reel-10 projects/<new> && cd projects/<new>      # node_modules is a symlink
# 1. write script/script.json (references/script-schema.md)
python3 scripts/draft_voice.py && DIALOGUE=script/dialogue.draft.mp3 python3 scripts/voice.py   # free edge-tts draft
python3 scripts/qa_report.py        # pacing, holds, reactions, caption speed, payoff %, unspoken word cues
node scripts/qa.mjs                 # a still per line → out/qa/sheet-*.png; read every sheet
# 2. real voice: ONE ElevenLabs v4 dialogue call
python3 scripts/dialogue.py         # prints the generate_audio params (tags + say, voices) → save result as script/dialogue.mp3
python3 scripts/voice.py && python3 scripts/qa_report.py
# 3. render (two-pass −14 LUFS) + spec gate
REEL_NAME=<NAME> node scripts/render-reel.mjs --no-voice       # FRAMES=0-240 for a quick check
bash plugins/motion-studio/skills/meta-delivery-qa/scripts/check_specs.sh out/<NAME>.mp4
```

- **Voice**: Higgsfield `generate_audio`, model `elevenlabs_v4`, `dialogue=[{text, voice_type, voice_id}]` + a one-paragraph direction `prompt`. Inline audio tags work (`[excited] [laughs] [gasps] [whispers] [jumping in] [worried] [warmly] [confident]`): put them in the line's `tags`, never in `say`. ~3 credits per reel. Whole conversation in one call; per-line TTS sounds stitched. `voice.py` cuts only quiet pauses (laughs survive), aligns Whisper word times to `say`, opens the payoff breath, ducks the pad.
- **Faces**: `scripts/faces.py who base.png closed=… open=… shock=… --mouth x0,y0,x1,y1 --face …` aligns AI-edited expression shots to the base bust and pastes only the mouth (talking) or the face (reactions), so frames never jitter. Edit prompts: "Keep everything identical… change ONLY the mouth / facial expression". ~2 credits per frame (Nano Banana via Higgsfield). Current set: aman `closed half open wink laugh surprised`, riya `closed half open shock laugh doubt worry`.
- **Sound effects**: `scripts/sfx.py` synthesizes `public/sfx/*.wav` with numpy (pop, tick, whoosh, swish, thump, ding, buzz, riser, huh, gasp, cash). No samples, no licences.
- **Countdowns**: `vars.countdown.to` makes `{days}` live on the board; rerun `voice.py` on the posting day (no new voice needed).

## QA gate (all must hold before delivery)

`qa_report.py` clean (or every WARN explained), every contact sheet read, spec check PASS, the approval file lists every claim as verified, and the post is labelled AI-generated in Instagram. Then write the posting kit (caption, pinned comment, auto-DM text, cover frame).

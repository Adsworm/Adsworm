# 04 · Cut plan, motion and B-roll

## Structure
- Find the strongest self-contained line, with no claim that needs context. Moving it to the front as a hook is fine if it is not repeated later and the order inside sentences is untouched. Offer chronological as the alternative.
- Testimonial archetype that worked: HOOK (emotion) → ORIGIN (how they found us) → EXPERIENCE (what was done) → PEOPLE (who helped) → RECOMMENDATION → logo end card.
- Cut only in real silences (≥150 ms, ideally ≥400 ms), found on the cleaned voice at 5–10 ms resolution. Snap to word boundaries and pad 30–200 ms. Keep breaths and hesitations that have no silent gap: cutting them is audible.

## Edit list (`edl.json`)
```json
{"fps":25,"segments":[
  {"id":"hook","in":389,"out":494,"face_at":[0.38,0.385],"zoom":[[389,1.34],[399,1.34],[412,1.46],[494,1.52]]},
  {"id":"open","in":47,"out":384,"face_at":[0.407,0.401],"zoom":[[47,1.04],[186,1.09],[200,1.20],[216,1.20],[230,1.30],[384,1.35]]},
  {"id":"close","in":493,"out":851,"face_at":[0.37,0.39],"zoom":[[493,1.54],[640,1.50],[684,1.50],[698,1.28],[718,1.28],[730,1.40],[851,1.47]]}],
 "grade":{…}, "plates_dir":"optional", "plate_strength":1.0}
```
- `in` and `out` are source frames (out exclusive). Contiguous source runs belong in ONE segment with zoom keyframes: an in-segment eased push or reframe is smoother than a cut.
- `face_at`: where the face sits in the output. Keep it in the band where every frame's crop stays inside the source; `render_base.py` reports clamped frames, which must be 0.

## Motion rules (shared by the creators researched)
- Always ease. Use smootherstep for camera moves and `Easing.bezier(0.16,1,0.3,1)` for text. Nothing linear and nothing bouncy on premium work.
- Push in on emotional or decision words ("amazing", "recommend"); reframe wider on a new thought; never zoom on every sentence.
- One continuous camera move beats several cuts when the source is a single take.
- Glitches, spins and whip-pans do not suit premium aesthetics, and transitions should not call attention to themselves.

## B-roll
- Use only client-supplied or properly licensed footage that matches what is said (a treatment mentioned → that treatment, no implied results). Never AI-generated "results" in a clinic testimonial.
- Place B-roll on the line that names the thing ("great services … HydraFacial and laser") and on the people line ("my consultation"), 1.5–3 s each, cut on words, with captions continuing over it.
- Do not lift B-roll from another edit that has captions burned in; ask for the raw clips.

# 09 · Lessons learned (each one cost a client round)

1. **"Restrained" is not "invisible".** v1 followed "natural, not over-edited" so literally that the client called it flat: no visible grade, a timid zoom, boxed captions, no music. A premium edit is noticeably better than the source in a single frame comparison. Show a before/after strip of 5 frames.
2. **Ask what "mic sound" means.** The client wanted a close, dry, noise-free voice. A gentle denoise left the room in. Lead with the strongest enhancer that keeps the words, and show the A/B with numbers.
3. **Generative tools change content.** Resemble Enhance rewrote the testimonial's sentences. Real-ESRGAN replacement smoothed skin like a beauty filter. Check words (ASR against reference) and texture (cheek high-pass) before accepting any AI step.
4. **Haze is often self-inflicted.** Bloom on a backlit subject, face brightening toward a bright wall, and a full-frame caption scrim all read as "hazy" to a client. Ablate the stages.
5. **The last word of the film is the most dangerous cut.** Verify the final out-point with isolated-window ASR on the rendered file; long-context ASR "hears" a word that the cut removed.
6. **Measure the music duck correctly.** Align stems first. Never trust a single-number readout that contradicts your ears or the design.
7. **Captions over white objects.** Check the hardest frame (accent colour over the brightest object), not an average frame.
8. **Same-size jump cuts.** When the hook is lifted from later in the take, the join back must change shot size by at least 15%.
9. **Client material beats ASR for names.** The team's earlier edit had the consultant's name; four ASR passes disagreed.
10. **Two variants = one picture.** When asked for a team-style version, change only the overlay, so the client compares typography, not grades.
11. **CPU budget on 4 cores.** Running AI plates, Remotion renders and a 4K picture render at once tripled wall time. Queue the heavy jobs; run text and QC work in parallel instead.
12. **Never publish client words in a public repo.** Scripts, templates and lessons are generic; transcripts, phrase files and media stay private.

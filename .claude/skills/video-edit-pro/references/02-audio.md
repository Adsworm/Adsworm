# 02 · Voice cleanup

## Order of operations (measured on a phone recording, 2–3 m from the speaker, 100 Hz hum + 390/420 Hz AC drone)
1. Mono sum, then high-pass at 115 Hz (2 × 12 dB/oct), below the speaker's fundamental. Check the fundamental first.
2. **Narrow notches on the measured lines only**: deep at the mains frequency, shallow (−8/−9 dB) on harmonics that fall inside the voice. Take frequencies from `audio_analyse.py`; never copy them from another shoot.
3. Speech enhancement. Results on the same file:

| Tool | Noise floor vs speech | Word accuracy vs reference | Verdict |
|---|---|---|---|
| DeepFilterNet3, 12 dB cap | −29 dB | unchanged | Too light for a client who wants "mic sound" |
| DeepFilterNet3, 30 dB cap | −47 dB | lost 4 words (proper nouns, "facial") | Smears quiet consonants |
| **ClearVoice MossFormer2_SE_48K** | **−47 to −51 dB** | **unchanged (only a filler differed)** | **Use this** |
| Resemble Enhance (generative) | −81 dB, studio-dry | **rewrote the sentence** into other words | Never on testimonials |
| WPE (2-mic) or spectral de-reverb | +0–2 dB drier | unchanged | Not worth it on this material |

4. After MossFormer2: a soft expander (`agate` ratio 2, range 0.32), body +2 dB at 190 Hz, −2.5 dB at 400 Hz, presence +2.5 dB at 3.2 kHz, air shelf +4 dB at 7 kHz, then `acompressor` 3:1. Normalise to −16 LUFS as a stem, and to −14 LUFS in the final mix.
5. Always score candidates with `scripts/asr_batch.py "<reference text>" a.wav b.wav …`. Reject anything that changes words.

## What cannot be fixed
- **Distance colouration** (the speaker 2–3 m from a phone) during speech. Only re-synthesis removes it, and re-synthesis changes words. Tell the user plainly. For future shoots, recommend a lavalier, or a phone within arm's reach and out of the backlight.
- Clipping: check `astats` Flat factor. If words are clipped, say which ones.

## Cuts in audio
- Assemble from the mastered stem with sample-accurate `atrim`. Merge contiguous source runs so there is no edit point where the source was continuous.
- Fades: 30 ms in and 15 ms out at joins. The final fade must not eat the last consonant: verify the last word with `probe_words.py` on the edited output.

## Optional on-device alternative
iPhone footage carries Apple's spatial audio. On the phone that shot it, Photos → Edit → Audio Mix → "Studio" isolates the voice with no upload. It is worth an A/B.

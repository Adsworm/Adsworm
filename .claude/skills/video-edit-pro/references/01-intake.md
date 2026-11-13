# 01 · Intake and transcript

## Inspect (before any plan)
- `ffprobe -show_streams -show_format`. Check:
  - **Rotation:** iPhone portrait arrives as 3840×2160 with `rotation=-90`; ffmpeg auto-rotates.
  - **Frame timing:** `avg_frame_rate` vs `r_frame_rate` reveals VFR; histogram the frame deltas.
  - **Colour:** transfer and primaries. iPhone SDR is bt709 tv-range. HDR (HLG/PQ) needs tone mapping first.
  - **Extra streams:** iPhones carry a 4-channel spatial-audio (APAC) stream that ffmpeg cannot decode; use stream `0:a:0`.
  - **GPS:** `com.apple.quicktime.location.ISO6709` is in the metadata. Every export uses `-map_metadata -1`.
- Loudness with `ebur128=peak=true`, clipping with `astats` (Flat factor, Peak count) and a full spectrogram (`showspectrumpic`).
- `scripts/audio_analyse.py <mono.wav>` reports:
  - steady tonal peaks (hum and its harmonics, AC drone);
  - band-by-band speech-to-noise;
  - a pause map;
  - a rough reverb estimate (use only phrase ends followed by real pauses).
- Exposure stability: `signalstats` every 25th frame (YAVG range). Sample neutral, skin and brand colours on a full-resolution still.
- Camera drift: phase-correlation on the background band (top 40% of the frame), not on the subject.
- Contact sheet every 3 s, plus a 4-frame strip of the first 2.5 s to see the camera settle.

## Transcript
- Run faster-whisper large-v3 locally with word timestamps (`scripts/transcribe.py`), on the original audio and on a cleaned version, with `auto` language. Run a forced-Hindi (or other) pass when code-switching is possible.
- Whisper word starts run 0.3–0.5 s early after a pause, and long-context passes **fill in words that are not there** (they hallucinated "uh", "you know" and a clipped "work"). For any word that matters, use `scripts/probe_words.py` on short isolated windows.
- Mark everything below 0.60 confidence, or anything that differs between passes, and list it for the user. Proper nouns are the usual failures. Compare with client material such as the team's earlier edit, the website or a price list. On the first job the team's edit spelled the consultant's name; four ASR passes gave four different names.

## Report to the user (before planning)
A table of measured facts (duration, frames, picture, camera, exposure, audio, noise type, SNR), the timestamped transcript with uncertain words marked, the retake and pause analysis, and the strongest opening line with its context.

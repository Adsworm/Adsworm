# 06 · Music and mix

## Sourcing (licence first)
- Read the licence in a real browser and save the text next to the project (`MUSIC_LICENCE_RECORD.txt`). For example, Mixkit Stock Music Free License allows social posts and online ads; it does not allow TV/radio, CDs, games or remixing into a music-only track.
- Meta Sound Collection is fine for Facebook/Instagram only and needs the user's login.
- Agency libraries (Artlist, Epidemic, Musicbed) give the cleanest licence. Ask whether the client has one.
- I cannot judge mood by ear. `scripts/music_screen.py` shortlists by measurement:
  - percussiveness (high-frequency transient ratio): low means no drums;
  - spectral centroid: low means warm;
  - tempo;
  - major-minus-minor key correlation: positive means uplifting;
  - level stability over the first 40 s.
- Deliver the main mix plus 2 alternates so the client picks by ear. On the first job the client chose the classical-piano alternate.

## Mix (`scripts/add_music.sh <video> <voice stem> <music> <out> [start_s]`)
- Bed 13–15 dB under the voice before ducking, then a sidechain duck (threshold 0.05, ratio 2.5, attack 80 ms, release 650 ms). Result: the music sits about 20–22 dB under her voice while she speaks.
- Under the end card the bed rises about 7 dB over 0.9 s, then fades over 1.5 s.
- Final loudness −14 LUFS, limiter at −2 dBFS, true peak about −3.7 dBFS after AAC.
- **Measuring the duck:** subtract the voice from the mix only after aligning by cross-correlation; the limiters add about 10 ms latency. Without alignment you will "measure" the music 18 dB *above* the voice. Our first heavy duck (ratio 6) buried the bed at −33 dB, which is inaudible.
- The picture is stream-copied when adding music, so audio iterations take seconds.

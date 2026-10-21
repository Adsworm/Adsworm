# ffmpeg recipes (tested with ffmpeg 6.1 on 1080p sources)

Add `-c:v libx264 -crf 18 -pix_fmt yuv420p` to every re-encode. The H.264 4:2:0 output is what Meta handles best.

**1. Reframe 16:9 → 9:16 with a blurred fill** (keeps the whole frame)
```bash
ffmpeg -i in.mp4 -filter_complex "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];[0]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy out_9x16.mp4
```

**2. Reframe 16:9 → 9:16 with a crop** (subject centered; change `x` to follow an off-center subject)
```bash
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy out_9x16.mp4
# off-center: crop=ih*9/16:ih:x=iw*0.6-ih*9/32:y=0
```

**3. Frame-accurate trim** (re-encodes; `-c copy` only cuts on keyframes)
```bash
ffmpeg -ss 1.5 -i in.mp4 -t 3 -c:v libx264 -crf 18 -c:a aac clip.mp4
```

**4. Join two clips with a crossfade** (offset = clip A duration − fade)
```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.4:offset=5.6[v];[0:a][1:a]acrossfade=d=0.4[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p joined.mp4
```
Other transitions: `wipeleft`, `slideup`, `smoothleft`, `circleopen`, `fadeblack`. Use hard cuts by default; transitions are seasoning.

**5. Burn captions in brand font, sitting in the Reels safe zone**
```bash
ffmpeg -i in_9x16.mp4 -vf "subtitles=captions.srt:fontsdir=./fonts:force_style='FontName=Inter Tight,Bold=1,FontSize=16,PrimaryColour=&H00FFFFFF,BackColour=&H99000000,BorderStyle=4,Outline=0,Shadow=0,Alignment=2,MarginV=106'" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy captioned.mp4
```
libass measures SRT styles on a 288-px-tall virtual canvas. `MarginV=106` puts the line just above the bottom 35% of a 9:16 frame, and `FontSize=16` comes out at about 107 px on 1920. Colors are `&HAABBGGRR`.

**6. Duck music under VO**
```bash
ffmpeg -i vo.mp4 -i music.m4a -filter_complex "[1:a]volume=0.6[m];[m][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[duck];[0:a][duck]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac mixed.mp4
```

**7. Find silences** (to cut dead air)
```bash
ffmpeg -i in.mp4 -af silencedetect=noise=-35dB:d=0.4 -f null - 2>&1 | grep silence_
```

**8. Speed change** (2×; `atempo` takes 0.5–2.0 per stage, so chain stages for more)
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p fast.mp4
```

**9. Apply a LUT**
```bash
ffmpeg -i in.mp4 -vf "lut3d=brand.cube" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy graded.mp4
```

**10. Audio for transcription** (whisper.cpp wants 16 kHz mono PCM)
```bash
ffmpeg -i in.mp4 -ar 16000 -ac 1 -c:a pcm_s16le vo.wav
```

**11. Put a transparent overlay** (Remotion ProRes 4444 lower-third or end card) **on top of footage**
```bash
ffmpeg -i footage.mp4 -i overlay.mov -filter_complex "[0][1]overlay=0:0:shortest=1" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy out.mp4
```

**12. Contact sheet of a source clip** (one frame per second, 6 tiles)
```bash
ffmpeg -i in.mp4 -vf "fps=1,scale=320:-1,tile=3x2" -frames:v 1 sheet.png
```

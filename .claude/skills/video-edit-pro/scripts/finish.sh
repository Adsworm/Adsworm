#!/usr/bin/env bash
# Composite the transparent overlay over the graded picture, add the mix, encode, strip metadata.
# Usage: finish.sh <base.mov> <overlay.mov> <mix.wav> <out> <social|master> <endcard_seconds> [title]
set -euo pipefail
BASE="$1"; OV="$2"; MIX="$3"; OUT="$4"; MODE="$5"; END="$6"; TITLE="${7:-}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OV")
FO=$(python3 -I -c "print(round($DUR-0.32,3))")
# Hold the last picture frame under the end card, overlay, soft fade from/to black at the very start and end.
VF="[0:v]tpad=stop_mode=clone:stop_duration=${END}[b];[1:v]format=yuva444p10le[ov];[b][ov]overlay=0:0:format=yuv444p10:alpha=straight:shortest=1,fade=t=in:st=0:d=0.20,fade=t=out:st=${FO}:d=0.32"
COL="-color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv"
if [ "$MODE" = social ]; then
  ffmpeg -v error -y -i "$BASE" -i "$OV" -i "$MIX" -filter_complex "${VF},format=yuv420p[v];[2:a]afade=t=in:d=0.03[a]" -map "[v]" -map "[a]" \
    -c:v libx264 -preset slow -crf 17 -maxrate 16M -bufsize 32M -profile:v high -level 4.2 -pix_fmt yuv420p $COL -r 25 \
    -c:a aac -b:a 256k -ar 48000 -movflags +faststart -map_metadata -1 -metadata title="$TITLE" -t "$DUR" "$OUT"
else
  # Master: composite once to ProRes 422 HQ (10-bit, PCM audio), then derive a compact 10-bit HEVC from it.
  # Doing both in one pass with x265 is several times slower on a 4-core machine.
  PRORES="${OUT%.*}_ProRes422HQ.mov"
  ffmpeg -v error -y -i "$BASE" -i "$OV" -i "$MIX" -filter_complex "${VF},format=yuv422p10le[v];[2:a]afade=t=in:d=0.03[a]" -map "[v]" -map "[a]" \
    -c:v prores_ks -profile:v 3 -vendor apl0 $COL -r 25 -c:a pcm_s24le -ar 48000 -map_metadata -1 -metadata title="$TITLE" -t "$DUR" "$PRORES"
  ffmpeg -v error -y -i "$PRORES" -map 0:v -map 0:a -c:v libx265 -preset fast -crf 13 -pix_fmt yuv420p10le -tag:v hvc1 \
    -x265-params "log-level=error:colorprim=bt709:transfer=bt709:colormatrix=bt709:range=limited" $COL -r 25 \
    -c:a pcm_s24le -map_metadata -1 -metadata title="$TITLE" "$OUT"
  ffprobe -v error -show_entries format=duration,size:stream=codec_name,profile,width,height,pix_fmt,nb_frames,color_space -of default=nw=1 "$PRORES" | tr '\n' ' '; echo
fi
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,pix_fmt,nb_frames,color_space -of default=nw=1 "$OUT" | tr '\n' ' '; echo

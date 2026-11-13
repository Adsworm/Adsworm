#!/usr/bin/env bash
# Add a licensed music bed under the finished voice track and remux. The picture is stream-copied (no re-encode).
# Usage: add_music.sh <video_in.mp4|mov> <voice_stem.wav> <music_file> <video_out> [music_start_seconds]
# Levels (measured on the first job): bed about 20 dB under the voice while she speaks (15 dB base + gentle ducking),
# Override with BED=<dB under voice> DUCK_THR=<linear> DUCK_RATIO=<n>. A heavy duck (ratio 6) made the bed inaudible.
# returns in pauses, lifts about 7 dB under the end card, then fades out over 1.5 s. Final mix -14 LUFS, peaks under -1.5 dB.
set -euo pipefail
VIN="$1"; VOICE="$2"; MUSIC="$3"; VOUT="$4"; MST="${5:-0}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE")
lufs(){ ffmpeg -hide_banner -nostats "$@" -af loudnorm=print_format=json -f null - 2>&1 | python3 -I -c "import sys,json; t=sys.stdin.read(); print(json.loads(t[t.rindex('{'):])['input_i'])"; }
ML=$(lufs -ss "$MST" -t "$DUR" -i "$MUSIC"); VL=$(lufs -i "$VOICE")
BED="${BED:-13}"; MG=$(python3 -I -c "print(round(($VL-$BED)-($ML),2))")        # music bed BED dB under the voice before ducking
END=$(python3 -I -c "print(round($DUR-2.6,2))"); FO=$(python3 -I -c "print(round($DUR-1.5,2))")
TMP="${VOUT%.*}_mix.wav"
ffmpeg -v error -y -i "$VOICE" -ss "$MST" -t "$DUR" -i "$MUSIC" -filter_complex "\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=${MG}dB,afade=t=in:d=0.6[m0];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[v][key];\
[m0][key]sidechaincompress=threshold=${DUCK_THR:-0.05}:ratio=${DUCK_RATIO:-2.5}:attack=80:release=650:knee=6:makeup=1[md];\
[md]volume='if(gte(t,${END}),min(2.4,1+1.4*(t-${END})/0.9),1)':eval=frame,afade=t=out:st=${FO}:d=1.5[m];\
[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.841:attack=5:release=80:level=disabled[o]" -map "[o]" -c:a pcm_s24le "$TMP"
G=$(python3 -I -c "print(round(-14-($(lufs -i "$TMP")),2))")
ffmpeg -v error -y -i "$TMP" -af "volume=${G}dB,alimiter=limit=0.794:attack=5:release=80:level=disabled" -c:a pcm_s24le "${TMP%.wav}_final.wav" && mv "${TMP%.wav}_final.wav" "$TMP"
case "$VOUT" in *.mov) AC="-c:a pcm_s24le";; *) AC="-c:a aac -b:a 256k";; esac
ffmpeg -v error -y -i "$VIN" -i "$TMP" -map 0:v -map 1:a -c:v copy $AC -movflags +faststart -map_metadata -1 -shortest "$VOUT"
echo "music gain ${MG} dB (music was ${ML} LUFS, voice ${VL} LUFS); final mix $(lufs -i "$TMP") LUFS -> $VOUT ; mix stem kept at $TMP"

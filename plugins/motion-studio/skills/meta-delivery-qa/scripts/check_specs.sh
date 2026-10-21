#!/usr/bin/env bash
# Checks a rendered ad against Meta delivery specs + Adsworm house rules.
#   check_specs.sh <file> [reels|stories|feed|square|landscape|auto]
# Exit 1 on any FAIL. WARN = best practice, not a platform rejection.
set -euo pipefail

file="${1:?usage: check_specs.sh <file> [placement]}"
placement="${2:-auto}"
fails=0
pass() { printf '  PASS  %s\n' "$1"; }
warn() { printf '  WARN  %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; fails=$((fails + 1)); }
gt() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a>b)}'; }

[[ -f "$file" ]] || { echo "no such file: $file"; exit 1; }
probe() { ffprobe -v error -select_streams "$1" -show_entries "$2" -of default=nw=1:nk=1 "$file" | head -1; }

codec=$(probe v:0 stream=codec_name)
[[ -n "$codec" ]] || { echo "no video stream"; exit 1; }
w=$(probe v:0 stream=width); h=$(probe v:0 stream=height)
pix=$(probe v:0 stream=pix_fmt); fps_raw=$(probe v:0 stream=r_frame_rate)
fps=$(awk -F/ '{printf "%.3f", $1/($2?$2:1)}' <<<"$fps_raw")
dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$file")
size=$(stat -c %s "$file" 2>/dev/null || stat -f %z "$file")
acodec=$(probe a:0 stream=codec_name || true)
ratio=$(awk -v w="$w" -v h="$h" 'BEGIN{printf "%.4f", w/h}')

if [[ "$placement" == auto ]]; then
  placement=$(awk -v r="$ratio" 'BEGIN{ if (r<0.6) print "reels"; else if (r<0.9) print "feed"; else if (r<1.2) print "square"; else print "landscape" }')
fi
case "$placement" in
  reels|stories) want=0.5625; label="9:16" ;;
  feed)          want=0.8;    label="4:5"  ;;
  square)        want=1;      label="1:1"  ;;
  landscape)     want=1.7778; label="16:9" ;;
  *) echo "unknown placement: $placement"; exit 1 ;;
esac

echo "$file → $placement ($label) · ${w}x${h} · ${codec}/${pix} · ${fps} fps · ${dur}s · $((size / 1024 / 1024)) MB · audio: ${acodec:-none}"

# Container + size
[[ "$file" =~ \.(mp4|mov|MP4|MOV)$ ]] && pass "container mp4/mov" || fail "container must be .mp4 or .mov"
gt "$size" 4294967296 && fail "file > 4 GB (Meta video ad max)" || pass "file size ≤ 4 GB"

# Geometry
awk -v r="$ratio" -v t="$want" 'BEGIN{d=r-t; if(d<0)d=-d; exit !(d/t<0.01)}' && pass "aspect $label" || fail "aspect ${w}x${h} is not $label for $placement"
short=$(( w < h ? w : h ))
(( short >= 1080 )) && pass "short edge ≥ 1080 px" || warn "short edge ${short}px < 1080 (soft on high-density phones)"

# Encoding
[[ "$codec" == h264 || "$codec" == hevc ]] && pass "codec $codec" || warn "codec $codec — H.264 is the safe default"
[[ "$pix" == yuv420p ]] && pass "pixel format yuv420p" || warn "pixel format $pix — use yuv420p (full-range/10-bit can shift color after re-encode)"
gt "$fps" 60.5 && fail "fps $fps > 60" || { gt "$fps" 30.5 && warn "fps $fps — 30 is enough for motion graphics and halves render time" || pass "fps $fps"; }

# Duration (best practice for performance, not platform limits)
case "$placement" in
  reels|stories) gt "$dur" 15.5 && warn "${dur}s — 9:16 ads that win usually land the offer by 15 s" || pass "duration ≤ 15 s" ;;
  *)             gt "$dur" 30.5 && warn "${dur}s — keep feed cuts ≤ 30 s unless it's a long-form story" || pass "duration ≤ 30 s" ;;
esac

# Audio
if [[ -z "${acodec:-}" ]]; then
  warn "no audio track — fine for silent-first, but sound-on placements reward music/VO"
else
  [[ "$acodec" == aac ]] && pass "audio aac" || warn "audio $acodec — AAC is the safe default"
  ebu=$(ffmpeg -nostats -hide_banner -i "$file" -filter_complex ebur128=peak=true -f null - 2>&1)
  loud=$(awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}' <<<"$ebu")
  peak=$(awk '/True peak/{f=1} f&&/Peak:/{print $2; exit}' <<<"$ebu")
  if [[ -n "$loud" ]]; then
    awk -v l="$loud" 'BEGIN{exit !(l>=-16 && l<=-12)}' && pass "loudness ${loud} LUFS" || warn "loudness ${loud} LUFS — target −14 (ffmpeg loudnorm=I=-14:TP=-1)"
    [[ -n "$peak" ]] && { gt "$peak" -1 && warn "true peak ${peak} dBTP > −1" || pass "true peak ${peak} dBTP"; }
  fi
fi

if (( fails )); then echo "RESULT: FAIL ($fails)"; exit 1; fi
echo "RESULT: PASS"

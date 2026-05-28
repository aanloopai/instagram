#!/usr/bin/env bash
# Konsept S master assemble — wipeleft transitions + logo swoosh overlay +
# subtitle burn-in + audio normalization.
#
# Pipeline:
#   1. 7 Veo shots concatenated with xfade=wipeleft 0.5s between each
#   2. logo_swoosh.png overlay slides L->R across frame during each xfade window
#   3. SRT subtitles burned in via subtitles filter (white outline + shadow)
#   4. Audio: acrossfade between shots (smooths embedded Veo audio)
#   5. Master export: H.264 CRF 18 + AAC 192k
#
# Output: assets/output/konsept_s_master.mp4 + konsept_s_master_subs.mp4
set -euo pipefail

DIR=assets/video/konsept_s/veo3
SWOOSH=assets/overlays/logo_swoosh.png
SRT=assets/subtitles/konsept_s.srt
OUT=assets/output/konsept_s_master.mp4
SUB_OUT=assets/output/konsept_s_master_subs.mp4

if ! command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG_BIN=$(ls -d /c/Users/Hallo/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)
  if [ -n "$FFMPEG_BIN" ]; then
    export PATH="$FFMPEG_BIN:$PATH"
  else
    echo 'ffmpeg not found'
    exit 1
  fi
fi

mkdir -p "$(dirname "$OUT")"

ffmpeg -y -v error \
  -i "$DIR/shot_01.mp4" -i "$DIR/shot_02.mp4" -i "$DIR/shot_03.mp4" \
  -i "$DIR/shot_04.mp4" -i "$DIR/shot_05.mp4" -i "$DIR/shot_06.mp4" \
  -i "$DIR/shot_07.mp4" \
  -loop 1 -i "$SWOOSH" \
  -filter_complex "
[0:v][1:v]xfade=transition=wipeleft:duration=0.5:offset=7.5[v01];
[v01][2:v]xfade=transition=wipeleft:duration=0.5:offset=15.0[v02];
[v02][3:v]xfade=transition=wipeleft:duration=0.5:offset=22.5[v03];
[v03][4:v]xfade=transition=wipeleft:duration=0.5:offset=30.0[v04];
[v04][5:v]xfade=transition=wipeleft:duration=0.5:offset=37.5[v05];
[v05][6:v]xfade=transition=wipeleft:duration=0.5:offset=45.0[vmain];
[7:v]format=rgba,fps=24[swoosh];
[vmain][swoosh]overlay=x='if(between(t,7.3,8.5),(t-7.3)/1.2*2160-1080,if(between(t,14.8,16.0),(t-14.8)/1.2*2160-1080,if(between(t,22.3,23.5),(t-22.3)/1.2*2160-1080,if(between(t,29.8,31.0),(t-29.8)/1.2*2160-1080,if(between(t,37.3,38.5),(t-37.3)/1.2*2160-1080,if(between(t,44.8,46.0),(t-44.8)/1.2*2160-1080,1080+W))))))':y=0:enable='between(t,7.3,8.5)+between(t,14.8,16.0)+between(t,22.3,23.5)+between(t,29.8,31.0)+between(t,37.3,38.5)+between(t,44.8,46.0)'[vout];
[0:a][1:a]acrossfade=d=0.5[a01];
[a01][2:a]acrossfade=d=0.5[a02];
[a02][3:a]acrossfade=d=0.5[a03];
[a03][4:a]acrossfade=d=0.5[a04];
[a04][5:a]acrossfade=d=0.5[a05];
[a05][6:a]acrossfade=d=0.5,loudnorm=I=-14:LRA=11:TP=-1[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUT"

echo "[OK] base master: $OUT"

if [ -f "$SRT" ]; then
  SRT_FF=$(cygpath -m "$(realpath "$SRT")" 2>/dev/null || echo "$SRT")
  ffmpeg -y -v error -i "$OUT" \
    -vf "subtitles='${SRT_FF//:/\\:}':force_style='FontName=Segoe UI,Bold=1,FontSize=42,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=4,Shadow=2,Alignment=2,MarginV=180'" \
    -c:a copy "$SUB_OUT"
  echo "[OK] with subtitles: $SUB_OUT"
else
  echo "[WARN] no SRT at $SRT — run scripts/generate_subtitles.py first"
fi

ls -lh "$OUT" "$SUB_OUT" 2>&1 || true

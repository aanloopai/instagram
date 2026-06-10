#!/usr/bin/env bash
# Konsept S v10 — clean rebuild: yalniz konusmacilar + sol-ust TV-bug logo.
# 0.2s crossfade her shot arasi. SRT BURN-IN ve SWOOSH OVERLAY YOK.
set -euo pipefail

DIR=assets/video/konsept_s/veo3
LOGO=assets/overlays/logo_tvbug_white.png
OUT=assets/output/konsept_s_v10_clean.mp4

if ! command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG_BIN=$(ls -d /c/Users/Hallo/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)
  if [ -n "$FFMPEG_BIN" ]; then
    export PATH="$FFMPEG_BIN:$PATH"
  else
    echo 'ffmpeg not found'; exit 1
  fi
fi

mkdir -p "$(dirname "$OUT")"

# 7 shot x 8s, 0.2s crossfade -> offset = N*(8-0.2) = N*7.8
ffmpeg -y -v error -stats \
  -i "$DIR/shot_01.mp4" -i "$DIR/shot_02.mp4" -i "$DIR/shot_03.mp4" \
  -i "$DIR/shot_04.mp4" -i "$DIR/shot_05.mp4" -i "$DIR/shot_06.mp4" \
  -i "$DIR/shot_07.mp4" \
  -framerate 24 -loop 1 -t 56 -i "$LOGO" \
  -filter_complex "
[0:v][1:v]xfade=transition=fade:duration=0.2:offset=7.8[v01];
[v01][2:v]xfade=transition=fade:duration=0.2:offset=15.6[v02];
[v02][3:v]xfade=transition=fade:duration=0.2:offset=23.4[v03];
[v03][4:v]xfade=transition=fade:duration=0.2:offset=31.2[v04];
[v04][5:v]xfade=transition=fade:duration=0.2:offset=39.0[v05];
[v05][6:v]xfade=transition=fade:duration=0.2:offset=46.8[vmain];
[7:v]format=rgba,scale=160:-1,colorchannelmixer=aa=0.75[logo];
[vmain][logo]overlay=x=40:y=40:format=auto:shortest=0[vout];
[0:a][1:a]acrossfade=d=0.2[a01];
[a01][2:a]acrossfade=d=0.2[a02];
[a02][3:a]acrossfade=d=0.2[a03];
[a03][4:a]acrossfade=d=0.2[a04];
[a04][5:a]acrossfade=d=0.2[a05];
[a05][6:a]acrossfade=d=0.2,loudnorm=I=-14:LRA=11:TP=-1[aout]" \
  -map "[vout]" -map "[aout]" \
  -t 54.8 \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUT"

echo "[OK] v10 clean master: $OUT"
ls -lh "$OUT"

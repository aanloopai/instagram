#!/usr/bin/env bash
# Konsept S v12 — wider uniform framing rebuild.
# Changes vs v11:
#  - Intro 0.4s fade-in (clean entry, no opening hitch).
#  - Robust audio: steady low bed (no sidechain pumping) so every speaker's
#    voice stays at a uniform level (fixes shot-2 speech dropout).
#  - Plain white shirt (no chest logo, per user).
# Inputs assumed already regenerated with wide/uniform framing.
set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG_BIN=$(ls -d /c/Users/Hallo/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)
  [ -n "$FFMPEG_BIN" ] && export PATH="$FFMPEG_BIN:$PATH" || { echo 'ffmpeg not found'; exit 1; }
fi

DIR=assets/video/konsept_s/veo3
LOGO=assets/overlays/logo_tvbug_white.png
BED=assets/audio/bed/bed.mp3
FONTB=assets/fonts/Inter-Bold.ttf
FONTS=assets/fonts/Inter-SemiBold.ttf
ENDCARD=assets/overlays/endcard.mp4
OUT=assets/output/konsept_s_v12.mp4
NAVY=0x0A1022

mkdir -p "$(dirname "$OUT")"

# 1) End card (2.6s): navy bg + centered white logo + CTA + url, fade-in.
ffmpeg -y -v error -f lavfi -i "color=c=${NAVY}:s=720x1280:r=24:d=2.6" \
  -loop 1 -t 2.6 -i "$LOGO" \
  -filter_complex "
[1:v]scale=560:-1[lg];
[0:v][lg]overlay=x=(W-w)/2:y=420[bg];
[bg]drawtext=fontfile=${FONTS}:text='Claim nu jouw gratis':fontcolor=0xC9D6E5:fontsize=40:x=(w-text_w)/2:y=720[t1];
[t1]drawtext=fontfile=${FONTB}:text='AI-Readiness Scan':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=775[t2];
[t2]drawtext=fontfile=${FONTS}:text='aanloopai.nl':fontcolor=0x8FA6BF:fontsize=38:x=(w-text_w)/2:y=900[t3];
[t3]fps=24,format=yuv420p,setsar=1,fade=t=in:st=0:d=0.4[v]" \
  -map "[v]" -t 2.6 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -an "$ENDCARD"
echo "[OK] endcard -> $ENDCARD"

# 2) Master: 7 shots xfade -> end card -> top-left logo + intro fade -> bed mix.
ffmpeg -y -v error -stats \
  -i "$DIR/shot_01.mp4" -i "$DIR/shot_02.mp4" -i "$DIR/shot_03.mp4" \
  -i "$DIR/shot_04.mp4" -i "$DIR/shot_05.mp4" -i "$DIR/shot_06.mp4" \
  -i "$DIR/shot_07.mp4" \
  -i "$ENDCARD" \
  -framerate 24 -loop 1 -t 60 -i "$LOGO" \
  -i "$BED" \
  -filter_complex "
[0:v][1:v]xfade=transition=fade:duration=0.2:offset=7.8[v01];
[v01][2:v]xfade=transition=fade:duration=0.2:offset=15.6[v02];
[v02][3:v]xfade=transition=fade:duration=0.2:offset=23.4[v03];
[v03][4:v]xfade=transition=fade:duration=0.2:offset=31.2[v04];
[v04][5:v]xfade=transition=fade:duration=0.2:offset=39.0[v05];
[v05][6:v]xfade=transition=fade:duration=0.2:offset=46.8,settb=1/24[vmain];
[7:v]fps=24,format=yuv420p,setsar=1,settb=1/24[ec];
[vmain][ec]xfade=transition=fade:duration=0.3:offset=54.5[vall];
[8:v]format=rgba,scale=160:-1,colorchannelmixer=aa=0.75[logo];
[vall][logo]overlay=x=40:y=40:format=auto:shortest=0,fade=t=in:st=0:d=0.4[vout];
[0:a][1:a]acrossfade=d=0.2[a01];
[a01][2:a]acrossfade=d=0.2[a02];
[a02][3:a]acrossfade=d=0.2[a03];
[a03][4:a]acrossfade=d=0.2[a04];
[a04][5:a]acrossfade=d=0.2[a05];
[a05][6:a]acrossfade=d=0.2[aspeech];
[aspeech]apad=whole_dur=57.2[spd];
[9:a]atrim=3:60.2,asetpts=N/SR/TB,volume=0.14[bedlow];
[spd][bedlow]amix=inputs=2:normalize=0:duration=longest[a0];
[a0]loudnorm=I=-14:LRA=11:TP=-1[aout]" \
  -map "[vout]" -map "[aout]" \
  -t 57.1 \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUT"

echo "[OK] v12 master: $OUT"
ls -lh "$OUT"

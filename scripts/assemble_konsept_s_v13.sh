#!/usr/bin/env bash
# Konsept S v13 — fully automated final.
# Same as v12 PLUS: shots 4-7 (closer/old framing) are auto-scaled to 85%
# and centered on a blurred full-bleed background so every speaker sits at a
# uniform distance — removes the manual CapCut step described in NOT.txt.
#  - shots 1,2,3 = wide framing (untouched).
#  - shots 4,5,6,7 = scaled to SCALE (default 0.85), blur-fill, centered.
set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG_BIN=$(ls -d /c/Users/Hallo/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)
  [ -n "$FFMPEG_BIN" ] && export PATH="$FFMPEG_BIN:$PATH" || { echo 'ffmpeg not found'; exit 1; }
fi

DIR=assets/video/konsept_s/veo3
SDIR=assets/video/konsept_s/veo3_scaled       # pre-scaled shots 4-7 land here
LOGO=assets/overlays/logo_tvbug_white.png
BED=assets/audio/bed/bed.mp3
FONTB=assets/fonts/Inter-Bold.ttf
FONTS=assets/fonts/Inter-SemiBold.ttf
ENDCARD=assets/overlays/endcard.mp4
OUT=assets/output/konsept_s_v13.mp4
NAVY=0x0A1022

# Framing match: 0.85 => person appears ~15% smaller (further away).
SCALE="${SCALE:-0.85}"
W=720; H=1280
FW=$(python -c "print(int(round($W*$SCALE/2))*2)")   # even foreground width
FH=$(python -c "print(int(round($H*$SCALE/2))*2)")   # even foreground height

mkdir -p "$(dirname "$OUT")" "$SDIR"

echo "[INFO] Foreground scale ${SCALE} -> ${FW}x${FH} on ${W}x${H} blur-fill."

# ---- Pre-pass: scale + blur-fill shots 4-7, keep their audio intact ----
for n in 04 05 06 07; do
  src="$DIR/shot_$n.mp4"
  dst="$SDIR/shot_$n.mp4"
  ffmpeg -y -v error -i "$src" -filter_complex "
[0:v]split=2[bg][fg];
[bg]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},boxblur=24:2,eq=brightness=-0.06:saturation=0.85[bgb];
[fg]scale=${FW}:${FH}[fgs];
[bgb][fgs]overlay=x=(W-w)/2:y=(H-h)/2,setsar=1,format=yuv420p[v]" \
    -map "[v]" -map 0:a -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
    -c:a aac -b:a 192k "$dst"
  echo "[OK] scaled shot_$n -> $dst"
done

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
#    Shots 1-3 from $DIR (wide), shots 4-7 from $SDIR (scaled blur-fill).
ffmpeg -y -v error -stats \
  -i "$DIR/shot_01.mp4" -i "$DIR/shot_02.mp4" -i "$DIR/shot_03.mp4" \
  -i "$SDIR/shot_04.mp4" -i "$SDIR/shot_05.mp4" -i "$SDIR/shot_06.mp4" \
  -i "$SDIR/shot_07.mp4" \
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

echo "[OK] v13 master: $OUT"
ls -lh "$OUT"

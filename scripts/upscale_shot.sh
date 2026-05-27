#!/usr/bin/env bash
# Real-ESRGAN ncnn-vulkan upscale pipeline (720x1280 -> 2880x5120 4x)
# Usage: bash scripts/upscale_shot.sh <input.mp4> <output.mp4> [scale=4] [model=realesrgan-x4plus]
set -euo pipefail

IN="${1:-assets/video/konsept_r/veo3/shot_01.mp4}"
OUT="${2:-assets/video/konsept_r/upscaled/shot_01_4x.mp4}"
SCALE="${3:-4}"
MODEL="${4:-realesrgan-x4plus}"

REALES_DIR=/c/Users/Hallo/tools/realesrgan
FFBIN=$(ls -d /c/Users/Hallo/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)
export PATH="$FFBIN:$PATH"

WORK=$(mktemp -d)
echo "[+] Workdir: $WORK"
mkdir -p "$WORK/in" "$WORK/out" "$(dirname "$OUT")"

echo "[1/3] Extract frames..."
ffmpeg -y -v error -i "$IN" "$WORK/in/frame_%05d.png"

echo "[2/3] Real-ESRGAN upscale (model=$MODEL scale=${SCALE}x, tile=128, single-thread for Intel Iris Xe)..."
"$REALES_DIR/realesrgan-ncnn-vulkan.exe" -i "$WORK/in" -o "$WORK/out" -s "$SCALE" -n "$MODEL" -t 128 -j 1:1:1 -f png 2>&1 | tail -5

echo "[3/3] Recompose video + audio..."
ffmpeg -y -v error -framerate 24 -i "$WORK/out/frame_%05d.png" -i "$IN" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy -map 0:v:0 -map 1:a:0 "$OUT"

rm -rf "$WORK"
echo "[OK] -> $OUT"
ls -lh "$OUT"

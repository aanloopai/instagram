#!/usr/bin/env bash
# Quick ffmpeg concat of 7 Veo talking-head shots for raw preview.
# No slides, no overlays, no grade — pure spine + embedded VO.
# Output: assets/output/konsept_r_concat_preview.mp4
set -euo pipefail

# Find ffmpeg (winget Gyan.FFmpeg default install path on Windows)
if ! command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG_BIN=$(ls -d /c/Users/*/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)
  if [ -n "$FFMPEG_BIN" ]; then
    export PATH="$FFMPEG_BIN:$PATH"
  else
    echo 'ffmpeg not found — install via: winget install Gyan.FFmpeg'
    exit 1
  fi
fi

OUT_DIR=assets/output
mkdir -p "$OUT_DIR"

LIST=$(mktemp --suffix=.txt)
PROJ_WIN=$(cygpath -w "$(pwd)" 2>/dev/null || pwd)
for i in 01 02 03 04 05 06 07; do
  PATH_WIN=$(cygpath -w "$(pwd)/assets/video/konsept_r/veo3/shot_$i.mp4" 2>/dev/null || echo "assets/video/konsept_r/veo3/shot_$i.mp4")
  echo "file '${PATH_WIN//\\/\\\\}'" >> "$LIST"
done

ffmpeg -y -f concat -safe 0 -i "$LIST" -c copy "$OUT_DIR/konsept_r_concat_preview.mp4"
echo "-> $OUT_DIR/konsept_r_concat_preview.mp4"
rm -f "$LIST"

"""
Logo + 4-stripe swoosh PNG for transition overlays.

Generates a horizontal swoosh element (full 1080x1920 RGBA transparent canvas
with aanloop AI logo in center + 4-color brand stripe spanning full width).
During xfade transitions, this PNG slides left-to-right across the frame to
"hand off" the brand between speakers.

Output: assets/overlays/logo_swoosh.png

Usage:
    python scripts/generate_logo_swoosh.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("assets/overlays")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

INDIGO  = (67, 56, 202)
ROSE    = (225, 29, 72)
AMBER   = (217, 119, 6)
EMERALD = (4, 120, 87)
WHITE   = (241, 245, 249)

FONT_BOLD_PATHS = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]


def find_font(size: int):
    for p in FONT_BOLD_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    band_h = 240
    band_top = (H - band_h) // 2
    band_bottom = band_top + band_h
    seg_w = W // 4
    for i, color in enumerate([INDIGO, ROSE, AMBER, EMERALD]):
        x0 = i * seg_w
        x1 = x0 + seg_w if i < 3 else W
        d.rectangle([x0, band_top, x1, band_bottom], fill=color + (255,))

    logo_text = "aanloop ai"
    font = find_font(140)
    bbox = d.textbbox((0, 0), logo_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (W - tw) // 2
    ty = band_top + (band_h - th) // 2 - 8
    pad = 28
    box_x0 = tx - pad
    box_y0 = ty - pad // 2
    box_x1 = tx + tw + pad
    box_y1 = ty + th + pad // 2
    d.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(11, 17, 32, 255))
    d.text((tx, ty), logo_text, font=font, fill=WHITE + (255,))

    out = OUTPUT_DIR / "logo_swoosh.png"
    img.save(str(out), "PNG", optimize=True)
    print(f"[OK] {out} ({W}x{H} RGBA)")


if __name__ == "__main__":
    main()

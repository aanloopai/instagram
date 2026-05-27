"""
Grid-paper slide compositor — Konsept R insert frames.

5 static 9:16 1080x1920 PNG cards, Revido-style white grid paper backdrop +
bold sans text + brand accent color. DaVinci timeline picks them up as
short-hold inserts between Veo 3 talking-head shots.

Slide list (per spec section 4 step 3):
  slide_01_risk_reversal   : "Dan krijg je elke euro terug." (blue accent)
  slide_02_eerste_20       : "De eerste 20 MKB'ers" (buildings glyph)
  slide_03_drie_kansen     : "drie grootste AI-kansen" (euro glyph)
  slide_04_urgency         : "Wees er snel bij" (red accent)
  slide_05_cta_card        : "Claim nu jouw / gratis AI-Readiness Scan / [CLAIM NU]"

Usage:
    python scripts/generate_slides.py             # all 5
    python scripts/generate_slides.py --slide 1   # one
"""
import argparse
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("assets/slides")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
BG = (252, 250, 245)
GRID = (220, 220, 215)
BLACK = (20, 20, 20)
BLUE = (37, 99, 235)
RED = (220, 38, 38)
MUTED = (110, 110, 110)
WHITE = (255, 255, 255)

FONT_BOLD_PATHS = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]
FONT_REG_PATHS = [
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
]


def find_font(paths, size: int) -> ImageFont.FreeTypeFont:
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_grid_bg(draw: ImageDraw.ImageDraw, step: int = 56) -> None:
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=GRID, width=1)


def center_lines(draw: ImageDraw.ImageDraw, lines, font, color, top: int, line_gap: int = 12) -> int:
    y = top
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((W - tw) / 2, y), line, font=font, fill=color)
        y += th + line_gap
    return y


def slide_base() -> tuple:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_grid_bg(draw)
    return img, draw


def slide_01_risk_reversal() -> Image.Image:
    img, draw = slide_base()
    f_big = find_font(FONT_BOLD_PATHS, 130)
    lines = ["Dan krijg je", "elke euro", "terug."]
    center_lines(draw, lines, f_big, BLUE, top=700, line_gap=20)
    return img


def slide_02_eerste_20() -> Image.Image:
    img, draw = slide_base()
    # Draw 3 line-art buildings (silhouettes), centered around y=800
    cx = W // 2
    base_y = 980
    blocks = [
        # (x_offset, width, height, window_rows)
        (-220, 130, 280, 5),
        (-50, 140, 360, 6),
        (130, 130, 240, 4),
    ]
    for dx, bw, bh, rows in blocks:
        x0 = cx + dx
        y0 = base_y - bh
        draw.rectangle([x0, y0, x0 + bw, base_y], outline=BLACK, width=8)
        # window grid (simple 2-col)
        win_w = (bw - 30) // 2 - 8
        win_h = (bh - 20) // rows - 8
        for row in range(rows):
            for col in range(2):
                wx = x0 + 15 + col * (win_w + 16)
                wy = y0 + 15 + row * (win_h + 8)
                draw.rectangle([wx, wy, wx + win_w, wy + win_h], fill=BLACK)
    # Ground line
    draw.line([(cx - 280, base_y + 6), (cx + 280, base_y + 6)], fill=BLACK, width=10)
    f_big = find_font(FONT_BOLD_PATHS, 88)
    lines = ["De eerste 20 MKB'ers", "die zich aanmelden"]
    center_lines(draw, lines, f_big, BLACK, top=1130, line_gap=14)
    return img


def slide_03_drie_kansen() -> Image.Image:
    img, draw = slide_base()
    f_icon = find_font(FONT_BOLD_PATHS, 260)
    glyph = "€"
    bbox = draw.textbbox((0, 0), glyph, font=f_icon)
    iw = bbox[2] - bbox[0]
    draw.text(((W - iw) / 2, 700), glyph, font=f_icon, fill=BLACK)
    f_big = find_font(FONT_BOLD_PATHS, 80)
    lines = ["Met de drie grootste", "AI-kansen voor", "hun bedrijf"]
    center_lines(draw, lines, f_big, BLACK, top=1090, line_gap=14)
    return img


def slide_04_urgency() -> Image.Image:
    img, draw = slide_base()
    f_big = find_font(FONT_BOLD_PATHS, 150)
    lines = ["Wees er", "snel bij."]
    center_lines(draw, lines, f_big, RED, top=820, line_gap=20)
    return img


def slide_05_cta_card() -> Image.Image:
    img, draw = slide_base()
    cx0, cy0, cx1, cy1 = 90, 380, W - 90, H - 380
    draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=40, fill=WHITE, outline=GRID, width=2)
    f_head = find_font(FONT_BOLD_PATHS, 110)
    headline_lines = ["Claim nu jouw", "gratis", "AI-Readiness Scan"]
    accent_idx = 1
    y = cy0 + 120
    for i, line in enumerate(headline_lines):
        color = BLUE if i == accent_idx else BLACK
        bbox = draw.textbbox((0, 0), line, font=f_head)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((W - tw) / 2, y), line, font=f_head, fill=color)
        y += th + 18
    f_sub = find_font(FONT_REG_PATHS, 56)
    sub = "Ontdek jouw AI-kans"
    bbox = draw.textbbox((0, 0), sub, font=f_sub)
    sw = bbox[2] - bbox[0]
    sh = bbox[3] - bbox[1]
    draw.text(((W - sw) / 2, y + 30), sub, font=f_sub, fill=MUTED)
    f_btn = find_font(FONT_BOLD_PATHS, 64)
    btn_text = "CLAIM NU"
    bbox = draw.textbbox((0, 0), btn_text, font=f_btn)
    btw = bbox[2] - bbox[0]
    bth = bbox[3] - bbox[1]
    pad_x, pad_y = 70, 30
    by0 = y + 30 + sh + 90
    bx0 = (W - (btw + pad_x * 2)) / 2
    bx1 = bx0 + btw + pad_x * 2
    by1 = by0 + bth + pad_y * 2
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=60, fill=BLACK)
    draw.text((bx0 + pad_x, by0 + pad_y - 6), btn_text, font=f_btn, fill=WHITE)
    return img


SLIDES = [
    ("slide_01_risk_reversal", slide_01_risk_reversal),
    ("slide_02_eerste_20", slide_02_eerste_20),
    ("slide_03_drie_kansen", slide_03_drie_kansen),
    ("slide_04_urgency", slide_04_urgency),
    ("slide_05_cta_card", slide_05_cta_card),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slide", type=int, help="Generate only this slide (1-5)")
    args = parser.parse_args()

    selected = SLIDES if args.slide is None else [SLIDES[args.slide - 1]]
    print(f"Generating {len(selected)} slide(s)\n")
    for name, fn in selected:
        out = OUTPUT_DIR / f"{name}.png"
        img = fn()
        img.save(str(out), "PNG", optimize=True)
        print(f"    -> {out}")

    print(f"\n[OK] Slides in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

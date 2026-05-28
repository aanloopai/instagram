"""
Wall-mounted embossed Aanloop logo PNG.

Generates a semi-transparent embossed monogram element to be overlaid on
all shots at a consistent position (top-right corner). Gives a "logo
mounted on the studio wall" appearance.

Output: assets/overlays/wall_logo.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path("assets/overlays/wall_logo.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

FONT_BOLD_PATHS = [
    "assets/fonts/Inter-Bold.ttf",
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

    logo_text = "aanloop ai"
    font = find_font(64)

    bbox = d.textbbox((0, 0), logo_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    margin = 50
    x = W - tw - margin
    y = margin + 20

    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow_layer)
    ds.text((x + 3, y + 3), logo_text, font=font, fill=(0, 0, 0, 140))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(shadow_layer, (0, 0), shadow_layer)

    highlight_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dh = ImageDraw.Draw(highlight_layer)
    dh.text((x - 1, y - 1), logo_text, font=font, fill=(255, 255, 255, 35))
    highlight_layer = highlight_layer.filter(ImageFilter.GaussianBlur(radius=1))
    img.paste(highlight_layer, (0, 0), highlight_layer)

    d.text((x, y), logo_text, font=font, fill=(220, 226, 235, 160))

    stripe_w = tw
    stripe_h = 5
    sx = x
    sy = y + th + 14
    colors = [(67, 56, 202), (225, 29, 72), (217, 119, 6), (4, 120, 87)]
    seg = stripe_w // 4
    for i, c in enumerate(colors):
        x0 = sx + i * seg
        x1 = sx + (i + 1) * seg if i < 3 else sx + stripe_w
        d.rectangle([x0, sy, x1, sy + stripe_h], fill=c + (180,))

    img.save(str(OUT), "PNG", optimize=True)
    print(f"[OK] {OUT}")


if __name__ == "__main__":
    main()

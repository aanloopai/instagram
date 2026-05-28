"""
Konsept S — 3 karakter Imagen 4 ultra sample.

Brand-fit Aanloop:
  - Navy backdrop #0B1120 (midnight)
  - 4-color stripe accent bar (subtle floor/horizon line)
      indigo #4338CA  rose #E11D48  amber #D97706  emerald #047857
  - Inter Bold reference for any visible typography
  - Studio creator setup, lavalier mic, consistent set across all chars

3 characters (Hollywood morph cast):
  man     : NL male, 32-36, mevcut narrator yaklasimi
  woman   : NL female, 30-35
  elderly : NL elderly male, 60-70, weathered, dignified

Output: assets/characters/konsept_s/{man,woman,elderly}_v{NN}.png

Usage:
    python scripts/generate_konsept_s_chars.py                    # 2/char = 6
    python scripts/generate_konsept_s_chars.py --char man --variants 4
"""
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/characters/konsept_s")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_MODEL = "imagen-4.0-ultra-generate-001"

BRAND_SET = (
    "Studio creator setup, clean minimalist set, deep midnight navy seamless "
    "backdrop filling entire background (very dark blue-black, almost slate, "
    "uniform smooth tone, no gradient banding). The backdrop is completely "
    "PLAIN — no stripes, no accent bars, no colored lines, no graphics, no "
    "objects, no text, no logos, no decorative elements anywhere. Just clean "
    "uniform dark navy wall. "
    "NO text, NO letters, NO numbers, NO hex codes, NO color labels, NO "
    "writing on any surface, NO stripes, NO color bars, NO accent lines, "
    "NO posters, NO frames, NO props, NO furniture. "
    "Cinematic cool studio lighting with a soft cool-neutral key light from "
    "front-left, gentle fill from front-right, subtle rim light separating "
    "subject from backdrop. 9:16 vertical 1080x1920."
)

QUALITY = (
    " Ultra-photorealistic professional commercial portrait, sharp focus on "
    "eyes with visible catchlights, shallow depth of field f/2.8 portrait "
    "compression, 85mm full-frame look, shot on Sony A7 IV, natural skin "
    "texture with realistic pores and subtle imperfections (NOT plastic, NOT "
    "oversmoothed, NOT doll-like, NOT uncanny valley), symmetric facial "
    "features, no AI artifacts, photojournalism realism."
)

CONSTRAINTS = (
    " Strict: one person only, no second subject, plain crisp white crew-neck "
    "cotton t-shirt (no logo no print), small black DPA-style lavalier "
    "microphone clipped to t-shirt collar clearly visible, no laptop, no "
    "desk, no hat, no sunglasses, no thick beard, no thick moustache, no "
    "tattoos, no jewelry."
)

CHARACTERS = {
    "man": (
        "Photoreal portrait of a Dutch male tech expert and AI consultant, "
        "34 years old, Northern European features, short medium-brown hair "
        "with subtle natural grey at temples, light well-groomed stubble, "
        "intelligent warm hazel eyes with direct eye contact to camera, "
        "confident relaxed friendly smile. "
    ),
    "woman": (
        "Photoreal full-body MEDIUM-WIDE PORTRAIT of a Dutch female business "
        "strategist and AI advisor, 32 years old, Northern European features, "
        "shoulder-length natural blonde hair styled loose with subtle natural "
        "movement, minimal natural makeup, intelligent warm blue-grey eyes "
        "with direct eye contact to camera, confident relaxed friendly smile. "
        "FRAMING IS WIDER: shot from waist up so both arms and hands are "
        "FULLY VISIBLE in frame. Her RIGHT HAND is raised, holding a modern "
        "smartphone clearly visible at chest level, smartphone screen tilted "
        "toward the camera showing an abstract dark-mode dashboard interface "
        "with subtle colored UI cards (NO readable text). Her left arm rests "
        "at her side. The smartphone is a clear visual prop, the hand and "
        "the phone occupy roughly 20 percent of the frame area at lower right. "
    ),
    "elderly": (
        "Photoreal portrait of a Dutch elderly male senior advisor and "
        "industry veteran, 67 years old, Northern European features, "
        "thick well-groomed silver-grey hair combed back, neat short silver-"
        "grey beard, weathered dignified face with visible character lines "
        "around the eyes and forehead, intelligent warm hazel eyes with "
        "direct eye contact to camera, calm confident knowing smile. "
    ),
}


def build_prompt(char_key: str, char_desc: str) -> str:
    return char_desc + BRAND_SET + QUALITY + CONSTRAINTS


def generate(client, char_key: str, variant: int, prompt: str, force: bool, model: str):
    from google.genai import types as gtypes
    out = OUTPUT_DIR / f"{char_key}_v{variant:02d}.png"
    if out.exists() and not force:
        print(f"    [=] Skip (exists): {out.name}")
        return out

    print(f"    [+] {char_key} variant {variant}")
    cfg = gtypes.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="9:16",
        person_generation=gtypes.PersonGeneration.ALLOW_ADULT,
        output_mime_type="image/png",
    )
    result = client.models.generate_images(model=model, prompt=prompt, config=cfg)
    if not result.generated_images:
        raise RuntimeError(f"No images (RAI? safety={result.positive_prompt_safety_attributes})")
    img = result.generated_images[0]
    if img.rai_filtered_reason:
        raise RuntimeError(f"RAI filtered: {img.rai_filtered_reason}")
    out.write_bytes(img.image.image_bytes)
    print(f"        -> {out}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--char", choices=list(CHARACTERS.keys()))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    chars = {args.char: CHARACTERS[args.char]} if args.char else CHARACTERS

    key = os.environ.get("GOOGLE_AI_STUDIO_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set")
        sys.exit(1)

    from google import genai
    client = genai.Client(api_key=key)

    total = len(chars) * args.variants
    print(f"Generating {total} Konsept S character portrait(s)\n")
    failures = []
    for ck, cd in chars.items():
        prompt = build_prompt(ck, cd)
        for v in range(1, args.variants + 1):
            try:
                generate(client, ck, v, prompt, args.force, args.model)
            except Exception as e:
                print(f"        [FAIL] {ck}_v{v:02d}: {e}")
                failures.append((ck, v, str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Konsept S character failures\n")
            for ck, v, msg in failures:
                f.write(f"- {ck}_v{v:02d}: {msg}\n")
        sys.exit(1)

    print(f"\n[OK] All {total} portraits in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

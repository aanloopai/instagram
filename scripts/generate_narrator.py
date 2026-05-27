"""
Imagen 4 ile Konsept R narrator (NL-male IT-expert) uret.

5 angle x N variant = N*5 portret. Default N=2 sample-mode, N=8 full-mode.

Prompt template: prompts/imagen/konsept_r_narrator.txt (master + per-angle delta).

Output: assets/characters/narrator/{angle}_v{NN}.png

Usage:
    python scripts/generate_narrator.py                  # sample mode (2/angle = 10 toplam)
    python scripts/generate_narrator.py --full           # 8/angle = 40 toplam
    python scripts/generate_narrator.py --angle frontal  # tek angle batch
    python scripts/generate_narrator.py --variants 4     # custom variant sayisi
"""
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/characters/narrator")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_PROMPT = (
    "Ultra-photorealistic 9:16 vertical commercial portrait photograph of a single "
    "Dutch male tech expert and AI consultant, 34 years old, alone, Northern "
    "European features, short medium-brown hair with subtle natural grey at the "
    "temples, light well-groomed stubble (no thick beard, no thick moustache), "
    "intelligent warm hazel eyes with direct eye contact to camera, symmetric "
    "facial features, confident relaxed smile (approachable not aggressive), clean "
    "fresh natural skin with realistic pores and subtle imperfections (not "
    "oversmoothed, not plastic, not doll-like, no uncanny valley), wearing a plain "
    "crisp white crew-neck cotton t-shirt (no logo, no print, no tattoos, no "
    "jewelry, no hat, no sunglasses), small black DPA-style lavalier microphone "
    "clipped to t-shirt collar clearly visible, medium close-up framing showing "
    "head and chest only (no hands visible, no laptop, no desk, no props), calm "
    "confident posture, slight head tilt, creator-studio YouTube setup, seamless "
    "burnt-orange / oxblood paper backdrop hex #a0301a filling entire background "
    "with no texture artifacts and no busy elements, soft three-point lighting "
    "with warm key light from front-left at 30 degrees, gentle fill from front-"
    "right, subtle rim light separating subject from background, sharp focus on "
    "eyes with visible catchlights, shallow depth of field f/2.8 portrait lens "
    "compression, 85mm full-frame look, shot on Sony A7 IV with 85mm f/1.4 GM, "
    "natural professional commercial photography style, photojournalism realism, "
    "1080x1920 vertical Reels aspect ratio. Strict: one person only, no second "
    "subject, no woman, no child, no elderly person."
)

NEGATIVE_PROMPT = (
    "plastic skin, oversmoothed face, doll-like, uncanny valley, asymmetric eyes, "
    "distorted features, extra fingers, melted ears, cartoon, 3d render, cgi, "
    "illustration, painting, anime, low resolution, blurry, jpeg artifacts, text, "
    "watermark, logo, fingers visible, hand visible, full body, wide shot, busy "
    "background, props, computer, laptop, desk, sunglasses, hat, beard full, "
    "moustache thick, tattoos, jewelry necklace, multiple subjects, two people, "
    "woman, female, elderly, child, teenager"
)

ANGLES = {
    "frontal": "",
    "three_quarter_left": (
        "head turned slightly to left at 15 degrees, eyes still engaging camera, "
        "three-quarter view showing left ear partially"
    ),
    "three_quarter_right": (
        "head turned slightly to right at 15 degrees, eyes still engaging camera, "
        "three-quarter view showing right ear partially"
    ),
    "profile_left": (
        "pure side profile, head turned 90 degrees left, looking off-camera at "
        "imaginary monitor, mouth closed"
    ),
    "wider": (
        "medium-wide shot showing chest and arms folded relaxed, same outfit and "
        "backdrop, hands visible folded across stomach calm"
    ),
}


def build_prompt(angle_key: str, angle_delta: str) -> str:
    if not angle_delta:
        return MASTER_PROMPT
    return MASTER_PROMPT.replace(
        "intelligent warm hazel eyes with direct eye contact to camera, ",
        f"intelligent warm hazel eyes, {angle_delta}, ",
    )


MODEL_ID = "imagen-4.0-ultra-generate-001"


def generate(client, angle_key: str, variant: int, prompt: str, force: bool) -> Path:
    out = OUTPUT_DIR / f"{angle_key}_v{variant:02d}.png"
    if out.exists() and not force:
        print(f"    [=] Skip (exists): {out.name}")
        return out

    from google.genai import types as gtypes

    print(f"    [+] {angle_key} variant {variant}")
    cfg = gtypes.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="9:16",
        person_generation=gtypes.PersonGeneration.ALLOW_ADULT,
        output_mime_type="image/png",
    )
    result = client.models.generate_images(model=MODEL_ID, prompt=prompt, config=cfg)
    if not result.generated_images:
        raise RuntimeError(f"No images returned (RAI filtered?). safety={result.positive_prompt_safety_attributes}")
    img = result.generated_images[0]
    if img.rai_filtered_reason:
        raise RuntimeError(f"RAI filtered: {img.rai_filtered_reason}")
    out.write_bytes(img.image.image_bytes)
    print(f"        -> {out}")
    return out


def main():
    global MODEL_ID
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="8 variants per angle (default 2)")
    parser.add_argument("--variants", type=int, default=None, help="Custom variant count per angle")
    parser.add_argument("--angle", choices=list(ANGLES.keys()), help="Generate only this angle")
    parser.add_argument("--force", action="store_true", help="Re-generate existing")
    parser.add_argument("--model", default=MODEL_ID, help=f"Imagen model id (default {MODEL_ID})")
    args = parser.parse_args()
    MODEL_ID = args.model

    variants = args.variants if args.variants else (8 if args.full else 2)
    angles = {args.angle: ANGLES[args.angle]} if args.angle else ANGLES

    key = os.environ.get("GOOGLE_AI_STUDIO_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set in .env")
        sys.exit(1)

    from google import genai
    client = genai.Client(api_key=key)

    total = len(angles) * variants
    print(f"Generating {total} narrator portraits ({len(angles)} angles x {variants} variants)")
    print(f"Model: {args.model}\n")

    failures = []
    for angle_key, angle_delta in angles.items():
        prompt = build_prompt(angle_key, angle_delta)
        for v in range(1, variants + 1):
            try:
                generate(client, angle_key, v, prompt, args.force)
            except Exception as e:
                print(f"        [FAIL] {angle_key}_v{v:02d}: {e}")
                failures.append((angle_key, v, str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Imagen 4 narrator failures\n")
            for ak, v, msg in failures:
                f.write(f"- {ak}_v{v:02d}: {msg}\n")
        print(f"\n[WARN] {len(failures)} failures logged to tasks/errors.md")
        sys.exit(1)

    print(f"\n[OK] All {total} portraits generated in {OUTPUT_DIR}")
    print("\nNext: pick best variant per angle, then run Veo 3 image-to-video.")


if __name__ == "__main__":
    main()

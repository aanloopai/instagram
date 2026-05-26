"""
Imagen 4 ile 5 karakter x 3 angle = 15 portre uret.
Kling Face Reference Library icin kaynak materyal.

Brief section 8.2 prompt template'i + 3 angle (frontal, 3/4, profile).

Output: assets/characters/{char}_{angle}.png

Usage:
    python scripts/generate_characters.py
    python scripts/generate_characters.py --force   # skip-existing kapali
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/characters")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTERS = {
    "destem": (
        "Dutch male, 35, Rotterdam multicultural heritage with subtle Mediterranean features, "
        "athletic build, wearing a sleek matte-black tactical headset wrapping from one ear "
        "down to the throat collar with a single subtle cyan light pulse on the throat plate, "
        "calm-warrior expression, composed, slight half-smile"
    ),
    "desecretaresse": (
        "Dutch female, 32, sharp clean features, dark hair in low bun, wearing a tailored "
        "charcoal trench coat with subtle holographic shoulder accents, holding a sleek "
        "glass tablet with soft cyan glow, confident composed expression"
    ),
    "destemvandesite": (
        "Dutch male, 27, lean build, wearing a deep hooded jacket with a glowing rune-style "
        "geometric emblem at the chest, mysterious composed expression, half face in shadow"
    ),
    "despeurder": (
        "Dutch female, 30, athletic, mid-length dark hair, wearing a sniper-style visor "
        "pushed up on her forehead, dark tactical vest with subtle red HUD glow accents, "
        "sharp focused gaze"
    ),
    "deleermeester": (
        "Dutch male, 55, salt-and-pepper hair, kind eyes, sophisticated charcoal blazer over "
        "high-neck top, holding a hybrid book/tablet object glowing softly, mentor expression"
    ),
}

ANGLES = {
    "frontal":      "facing camera directly, eye-level shot, direct eye contact",
    "threequarter": "3/4 turned to camera-left, eye contact maintained with camera",
    "profile":      "side profile facing camera-right, looking off-frame",
}

BASE_STYLE = (
    "Cinematic portrait. Neutral charcoal background. Shot on ARRI Alexa, 50mm lens, f/2.0. "
    "Warm key light from camera-right, soft fill from left. ARRI color science, oxblood and "
    "teal palette. Hyper-realistic, photorealistic, editorial fashion photography quality. "
    "No logos, no brand marks, no text. Aspect ratio 1:1."
)


def build_prompt(char_desc: str, angle_desc: str) -> str:
    return f"{char_desc}, {angle_desc}. {BASE_STYLE}"


def generate_portrait(char_key: str, angle_key: str, prompt: str, force: bool) -> Path:
    out = OUTPUT_DIR / f"{char_key}_{angle_key}.png"
    if out.exists() and not force:
        print(f"    [=] Skip (exists): {out.name}")
        return out

    import google.generativeai as genai

    print(f"    [+] {char_key} / {angle_key}")
    candidates = ["generate_image", "generate_images", "imagen", "Imagen"]
    fn = next((getattr(genai, name, None) for name in candidates if getattr(genai, name, None)), None)
    if fn is None:
        raise RuntimeError(
            "Imagen 4 entry point not found in google.generativeai. "
            "Run scripts/verify_apis.py and update the candidate list."
        )

    result = fn(
        model="imagen-4.0-generate-preview",
        prompt=prompt,
        aspect_ratio="1:1",
        number_of_images=1,
    )

    image_obj = result.images[0] if hasattr(result, "images") else result
    image_obj.save(str(out))
    print(f"        -> {out}")
    return out


def main():
    force = "--force" in sys.argv
    key = os.environ.get("GOOGLE_AI_STUDIO_KEY")
    if not key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set in .env")
        sys.exit(1)

    import google.generativeai as genai
    genai.configure(api_key=key)

    total = len(CHARACTERS) * len(ANGLES)
    print(f"Generating {total} portraits ({len(CHARACTERS)} chars x {len(ANGLES)} angles)\n")

    failures = []
    for char_key, char_desc in CHARACTERS.items():
        for angle_key, angle_desc in ANGLES.items():
            try:
                prompt = build_prompt(char_desc, angle_desc)
                generate_portrait(char_key, angle_key, prompt, force)
            except Exception as e:
                print(f"        [FAIL] {char_key}_{angle_key}: {e}")
                failures.append((char_key, angle_key, str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Imagen 4 failures\n")
            for ck, ak, msg in failures:
                f.write(f"- {ck}_{ak}: {msg}\n")
        print(f"\n[WARN] {len(failures)} failures logged to tasks/errors.md")
        sys.exit(1)

    print(f"\n[OK] All {total} portraits generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

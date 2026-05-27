"""
Imagen 4 UI mockup compositor — Konsept R floating laptop UI overlays.

Revido-style floating product UI screenshots (perspective-tilted in DaVinci on
top of blurred narrator BG). 3 mockups:
  mockup_01_marco_dashboard : Marco AI sales-agent calling lead live
  mockup_02_emma_chat       : Emma AI assistant drafting email reply
  mockup_03_ai_readiness    : AI-Readiness Scan landing card

Output: assets/ui/mockup_##_*.png (16:9 landscape, 1920x1080)
Imagen model: imagen-4.0-ultra-generate-001 (matches narrator quality)

Usage:
    python scripts/generate_ui_mockups.py             # all 3
    python scripts/generate_ui_mockups.py --mock 1    # one
"""
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/ui")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_MODEL = "imagen-4.0-ultra-generate-001"

MOCKUPS = [
    {
        "id": 1,
        "name": "marco_dashboard",
        "prompt": (
            "Ultra-photorealistic landscape 16:9 laptop screen UI screenshot of a "
            "modern Dutch AI sales-agent dashboard called 'Marco', clean minimal "
            "Tailwind-style web app design, dark navy header reading 'Marco - AI "
            "Salesagent', main panel showing an active phone call card with green "
            "live-call indicator dot, caller name 'Jan de Vries' and company "
            "'Bakkerij Janssen', call duration timer '00:23' in white digital "
            "font, three side panels left showing today's stats 'Gebeld: 47', "
            "'Afspraken: 6', 'Conversion: 12.7%' in bold numbers with small Dutch "
            "labels, transcript bubble at bottom showing live transcribed Dutch "
            "speech 'Goedemiddag, met Marco van Bakkerij Janssen...', subtle blue "
            "accent color #2563eb on highlight elements, white background main "
            "area, soft material-design shadows, premium SaaS dashboard "
            "aesthetic, sharp focus, screen pixels invisible, no laptop bezel "
            "around screen content (screen content only fills the frame), 1920x"
            "1080 landscape aspect ratio. Strict: realistic UI not stylized 3d "
            "illustration, no logos other than the word 'Marco', no faces in "
            "the screen, only the dashboard interface."
        ),
    },
    {
        "id": 2,
        "name": "emma_chat",
        "prompt": (
            "Ultra-photorealistic landscape 16:9 laptop screen UI screenshot of a "
            "modern Dutch AI email assistant interface called 'Emma', clean "
            "minimal Tailwind-style web app design, split view with email inbox "
            "list on the left (3 unread email rows with subject lines in Dutch "
            "such as 'Offerte aanvraag', 'Vraag over levering', 'Afspraak "
            "bevestigen') and on the right a draft email reply panel with "
            "headline 'Emma's voorgestelde reactie' (Emma's suggested reply), "
            "the draft Dutch email body visible with three paragraphs of "
            "natural Dutch business writing, two action buttons at bottom right "
            "'Verstuur' (black filled) and 'Bewerken' (outlined gray), small "
            "status indicator at top right reading 'Emma actief - 247 e-mails "
            "afgehandeld vandaag' in subtle gray text, blue accent color "
            "#2563eb on send button hover state, white background main area, "
            "soft material-design shadows, premium SaaS aesthetic, sharp focus, "
            "no laptop bezel around screen content, 1920x1080 landscape. "
            "Strict: realistic UI not stylized 3d illustration, no logos other "
            "than the word 'Emma', no faces in the screen."
        ),
    },
    {
        "id": 3,
        "name": "ai_readiness",
        "prompt": (
            "Ultra-photorealistic landscape 16:9 laptop screen UI screenshot of a "
            "Dutch SaaS landing page section titled 'Gratis AI-Readiness Scan', "
            "clean minimal Tailwind-style design, bold black headline 'Ontdek "
            "de drie grootste AI-kansen voor jouw MKB' centered top, sub-"
            "paragraph in Dutch reading 'Vul het formulier in en ontvang binnen "
            "48 uur een persoonlijk AI-plan', a clean web form with three input "
            "fields labeled 'Bedrijfsnaam', 'E-mailadres', 'Aantal werknemers' "
            "and a large black CTA button 'Claim mijn gratis scan' with white "
            "text, three subtle benefit bullets below the form reading "
            "'Persoonlijk plan', '48u response', 'Geen verplichtingen' in light "
            "gray Dutch text with blue check icons, small testimonial card at "
            "bottom right with placeholder avatar circle and rating five stars, "
            "white background main area, blue accent color #2563eb on links and "
            "checks, soft material-design shadows, premium SaaS landing "
            "aesthetic, sharp focus, no laptop bezel around screen content, "
            "1920x1080 landscape. Strict: realistic web UI not stylized 3d "
            "illustration, no logos visible, no faces in the screen."
        ),
    },
]


def generate(client, mockup: dict, model: str, force: bool):
    from google.genai import types as gtypes
    out = OUTPUT_DIR / f"mockup_{mockup['id']:02d}_{mockup['name']}.png"
    if out.exists() and not force:
        print(f"    [=] Skip (exists): {out.name}")
        return out

    print(f"    [+] Mockup {mockup['id']:02d} {mockup['name']}")
    cfg = gtypes.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
        person_generation=gtypes.PersonGeneration.DONT_ALLOW,
        output_mime_type="image/png",
    )
    result = client.models.generate_images(model=model, prompt=mockup["prompt"], config=cfg)
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
    parser.add_argument("--mock", type=int, help="Generate only this mockup (1-3)")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    key = os.environ.get("GOOGLE_AI_STUDIO_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set")
        sys.exit(1)

    from google import genai
    client = genai.Client(api_key=key)

    selected = [m for m in MOCKUPS if args.mock is None or m["id"] == args.mock]
    if not selected:
        print(f"[FAIL] mockup {args.mock} not in 1-{len(MOCKUPS)}")
        sys.exit(1)

    print(f"Generating {len(selected)} UI mockup(s) via {args.model}\n")
    failures = []
    for m in selected:
        try:
            generate(client, m, args.model, args.force)
        except Exception as e:
            print(f"        [FAIL] mockup_{m['id']:02d}: {e}")
            failures.append((m['id'], str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## UI mockup failures\n")
            for mid, msg in failures:
                f.write(f"- mockup_{mid:02d}: {msg}\n")
        sys.exit(1)

    print(f"\n[OK] All {len(selected)} mockups in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

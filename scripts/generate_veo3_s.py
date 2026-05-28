"""
Veo 3.1-fast image-to-video — Konsept S (Hollywood Morph cast).

3 karakter rotated across 7 shot. Each shot 8s. Hollywood face-morph
transitions (1s each) added in DaVinci between speaker changes.

Marco/Emma logic fix: shot 2 introduces them as AI-collega examples BEFORE
later shots reference them (no listener confusion).

Cast canonical refs:
  assets/characters/konsept_s/man.png      (NL male 34, hook + brand + CTA)
  assets/characters/konsept_s/woman.png    (NL female 32, guarantee + mechanism)
  assets/characters/konsept_s/elderly.png  (NL elderly 67, offer + social proof)

Output: assets/video/konsept_s/veo3/shot_##.mp4

Usage:
    python scripts/generate_veo3_s.py --shot 1            # test single
    python scripts/generate_veo3_s.py                     # all 7
    python scripts/generate_veo3_s.py --model veo-3.0-fast-generate-001
"""
import argparse
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/video/konsept_s/veo3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REF_DIR = Path("assets/characters/konsept_s")

DEFAULT_MODEL = "veo-3.1-fast-generate-preview"

SHARED_VEO_TAIL = (
    " Same outfit (plain white t-shirt with black lavalier microphone), same "
    "deep midnight navy plain seamless backdrop (uniform dark blue-black, NO "
    "stripes, NO color bars, NO accent lines, NO graphics, NO text, NO logos "
    "in the scene), same cool cinematic studio lighting (cool-neutral key "
    "from front-left, gentle fill, subtle rim light), locked-off medium "
    "close-up camera, 9:16 vertical frame. "
    "ABSOLUTE IDENTITY LOCK: every single frame of this shot shows EXACTLY "
    "the same face from the reference image. The face does NOT change, "
    "morph, drift, age, or shift even slightly between frames. Same exact "
    "face proportions, same skin tone and texture, same hair color and "
    "style, same eye shape and color, same nose, same jawline, same mouth "
    "shape, same chin, same forehead. Treat the reference image like a "
    "locked appearance template — only the head pose and lips animate, "
    "everything else about the face stays mathematically identical. "
    "MOUTH DISCIPLINE: speaks like a real person on an indoor podcast, not a "
    "theatrical actor. Natural conversational lip movement, SUBTLE lip "
    "shapes. Mouth barely opens for most syllables. Jaw stays nearly closed "
    "on soft consonants. NO exaggerated jaw drop. NO over-articulated "
    "speech. NO shouting. NO mouth-wide-open vowels. Voice is calm "
    "controlled conversational volume, normal speaking energy. "
    "MICRO-MOVEMENT: very subtle head movement, almost still, no exaggerated "
    "nods or tilts, no big head turns. Natural eye blinks every 3-4 seconds. "
    "Hands not visible. No body movement below shoulders. No camera shake. "
    "SEAMLESS CUT POSE: starts and ends the shot with a relaxed neutral "
    "expression and mouth nearly closed (ready for Hollywood face-morph "
    "transition to next character). "
    "Studio quiet, no background music in audio, only the spoken Dutch line."
)

SHOTS = [
    {
        "id": 1,
        "char": "man",
        "duration": 8,
        "vo": "Geen lead, geen e-mail, geen taak blijft meer liggen in jouw MKB.",
        "prompt": (
            "The man in the reference image, exact same identity, speaks "
            "directly to camera in Dutch with calm confident creator-style "
            "delivery. Subtle assured expression, mouth barely opening, like "
            "a quiet promise. Energy 7 out of 10."
        ),
    },
    {
        "id": 2,
        "char": "man",
        "duration": 8,
        "vo": "Bij AanloopAI bouwen wij AI-collega's voor jou. Marco belt jouw leads. Emma handelt je e-mail af. Vierentwintig uur per dag.",
        "prompt": (
            "The man in the reference image, same identity. Calm confident "
            "delivery. On 'AanloopAI' (pronounced 'AAN-loop-ai') slight "
            "forward intent. On 'Marco' and 'Emma' subtle warm smile. On "
            "'24 uur per dag' measured finality. Energy 7 out of 10. Ends "
            "with mouth nearly closed ready for cut."
        ),
    },
    {
        "id": 3,
        "char": "woman",
        "duration": 8,
        "vo": "Vanaf je telefoon zie je elke afspraak, elke lead, elk detail. Real-time, vanaf elke plek.",
        "prompt": (
            "The woman in the reference image, exact same identity. She holds "
            "the smartphone clearly in her right hand at chest level, screen "
            "tilted toward the camera (same as the reference image). She "
            "speaks directly to camera. On 'Vanaf je telefoon' she briefly "
            "and subtly tilts the phone slightly more toward camera (a small "
            "show-the-screen gesture). On 'elke afspraak, elke lead, elk "
            "detail' confident knowing smile. On 'vanaf elke plek' calm "
            "assured close. Phone stays clearly visible throughout. Energy "
            "7 out of 10. Mouth controlled, minimal opening."
        ),
    },
    {
        "id": 4,
        "char": "woman",
        "duration": 8,
        "vo": "Geen werk blijft hangen. Alle informatie binnen handbereik.",
        "prompt": (
            "The woman in the reference image, same identity. The phone "
            "stays in her hand resting at chest level (visible but not "
            "actively gestured). Calm authoritative claim. On 'Geen werk "
            "blijft hangen' firm confident head movement. On 'binnen "
            "handbereik' subtle warm smile, mouth controlled. Energy 7 out "
            "of 10. Ends with mouth closed."
        ),
    },
    {
        "id": 5,
        "char": "elderly",
        "duration": 8,
        "vo": "We bieden tijdelijk een gratis AI-Readiness Scan. De eerste 20 MKB'ers krijgen binnen 48 uur de drie grootste AI-kansen voor hun bedrijf.",
        "prompt": (
            "The elderly man in the reference image, exact same identity, "
            "frontal medium close-up. STARTS shot with mouth closed and "
            "neutral expression (Hollywood morph arrives at his face). "
            "Calm authoritative delivery befitting a senior advisor. On "
            "'gratis AI-Readiness Scan' subtle warm smile (offer reveal). "
            "On 'eerste 20 MKB'ers' confident slight nod. On '48 uur' "
            "delivery slows imperceptibly for clarity. Energy 7 out of 10."
        ),
    },
    {
        "id": 6,
        "char": "elderly",
        "duration": 8,
        "vo": "Onze AI-collega's werken 24/7, missen nooit een lead, en klanten geven ons 4,9 uit 5 sterren.",
        "prompt": (
            "The elderly man in the reference image, same identity. Closes "
            "the social-proof section. On '24/7' (spoken 'vierentwintig "
            "zeven') subtle head-nod of permanence. On 'missen nooit een "
            "lead' firm slight head shake of certainty. On '4,9 uit 5 "
            "sterren' (spoken 'vier-komma-negen uit vijf sterren') matter-"
            "of-fact knowing smile. Energy 7 out of 10. Ends with mouth "
            "closed for return morph to first man."
        ),
    },
    {
        "id": 7,
        "char": "man",
        "duration": 8,
        "vo": "Wil jij ontdekken hoe AI jouw MKB altijd up-to-date kan houden? Claim nu jouw gratis AI-Readiness Scan.",
        "prompt": (
            "The man in the reference image, exact same identity as in shot "
            "1 and 2 (return after morph from elderly). STARTS shot with "
            "mouth closed neutral expression (morph arrives back to him). "
            "The closer of the ad. On 'Dus wil jij ontdekken hoe AI' head "
            "tilts a fraction toward camera (direct address). On 'Claim nu' "
            "delivery sharpens into clean call-to-action, slight forward "
            "intent, confident smile, eyes locked to camera. Energy 7 build "
            "to 9 out of 10 on CTA. NOT shouted."
        ),
    },
]


def load_ref_image(char_key: str):
    from google.genai import types as gtypes
    path = REF_DIR / f"{char_key}.png"
    if not path.exists():
        raise FileNotFoundError(f"Ref missing: {path}. Run `make chars-s` first + canonical-rename.")
    return gtypes.Image(image_bytes=path.read_bytes(), mime_type="image/png")


def generate_shot(client, shot: dict, model: str, force: bool, poll_seconds: int = 15) -> Path:
    from google.genai import types as gtypes

    sid = shot["id"]
    out = OUTPUT_DIR / f"shot_{sid:02d}.mp4"
    if out.exists() and not force:
        print(f"    [=] Skip (exists): {out.name}")
        return out

    full_prompt = shot["prompt"] + SHARED_VEO_TAIL + f"\n\nSpoken Dutch line: \"{shot['vo']}\""
    print(f"    [+] Shot {sid:02d} ({shot['duration']}s, char={shot['char']}) — submitting…")
    ref_image = load_ref_image(shot["char"])

    cfg = gtypes.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=shot["duration"],
        aspect_ratio="9:16",
    )

    op = client.models.generate_videos(model=model, prompt=full_prompt, image=ref_image, config=cfg)
    elapsed = 0
    while not op.done:
        time.sleep(poll_seconds)
        elapsed += poll_seconds
        op = client.operations.get(op)
        print(f"        polling… {elapsed}s elapsed, done={op.done}")
        if elapsed > 600:
            raise TimeoutError(f"Shot {sid} polling exceeded 10min")

    if op.error:
        raise RuntimeError(f"Veo error: {op.error}")
    if not op.result or not op.result.generated_videos:
        raise RuntimeError(f"Veo returned no video (RAI?)")

    video = op.result.generated_videos[0].video
    if hasattr(video, "video_bytes") and video.video_bytes:
        out.write_bytes(video.video_bytes)
    elif hasattr(video, "uri") and video.uri:
        data = client.files.download(file=video)
        out.write_bytes(data)
    else:
        raise RuntimeError(f"No video bytes/URI: {video}")
    print(f"        -> {out}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shot", type=int, help="Generate only this shot (1-7)")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--poll", type=int, default=15)
    parser.add_argument("--rate-delay", type=int, default=60, help="Sleep seconds between consecutive shots (rate-limit avoidance)")
    args = parser.parse_args()

    key = os.environ.get("GOOGLE_AI_STUDIO_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set")
        sys.exit(1)

    from google import genai
    client = genai.Client(api_key=key)

    selected = [s for s in SHOTS if args.shot is None or s["id"] == args.shot]
    if not selected:
        print(f"[FAIL] shot {args.shot} not in 1-{len(SHOTS)}")
        sys.exit(1)

    total = sum(s["duration"] for s in selected)
    print(f"Generating {len(selected)} Konsept S Veo shot(s), total {total}s of video.")
    print(f"Model: {args.model}\n")

    failures = []
    for idx, shot in enumerate(selected):
        if idx > 0 and args.rate_delay > 0:
            print(f"        sleeping {args.rate_delay}s before next shot (rate-limit)…")
            time.sleep(args.rate_delay)
        try:
            generate_shot(client, shot, args.model, args.force, args.poll)
        except Exception as e:
            print(f"        [FAIL] shot_{shot['id']:02d}: {e}")
            failures.append((shot["id"], str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Veo Konsept S failures\n")
            for sid, msg in failures:
                f.write(f"- shot_{sid:02d}: {msg}\n")
        sys.exit(1)

    print(f"\n[OK] All {len(selected)} shots in {OUTPUT_DIR}")
    print("\nNext: DaVinci assemble with Hollywood morph transitions + Suno bed music continuous.")


if __name__ == "__main__":
    main()

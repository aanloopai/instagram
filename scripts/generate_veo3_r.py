"""
Veo 3 omni image-to-video generation — Konsept R (7 talking-head shot).

Pipeline: Imagen 4 narrator portret + Veo 3 omni prompt + NL VO (in prompt) =
8-11s talking-head MP4 with native audio + lip-sync.

Source of truth: prompts/veo3-i2v/shot_##.txt (developer docs).
This script: hardcoded SHOTS list keeps Veo prompt + ref-image + duration +
VO transcript in one place for execution.

Output: assets/video/konsept_r/veo3/shot_##.mp4

Usage:
    python scripts/generate_veo3_r.py --shot 1            # single shot test
    python scripts/generate_veo3_r.py                     # all 7 shots
    python scripts/generate_veo3_r.py --model veo-3.1-fast-generate-preview
    python scripts/generate_veo3_r.py --force             # re-generate existing

Cost note (per Google AI Studio Max plan, May 2026):
  veo-3.0-generate-001 (default): included in Max plan, $0 incremental
  veo-3.1-generate-preview      : per-second metered, ~$0.50/s = ~$30 for 7 shot
"""
import argparse
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/video/konsept_r/veo3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REF_DIR = Path("assets/characters/narrator")

DEFAULT_MODEL = "veo-3.0-generate-001"

SHARED_VEO_TAIL = (
    " Same outfit (white t-shirt with black lavalier microphone), same burnt-"
    "orange oxblood backdrop, single warm key light from front-left, locked-off "
    "medium close-up camera, 9:16 vertical frame. "
    "STRICT IDENTITY LOCK: his face remains visually identical to the reference "
    "photo throughout the entire shot — same exact face proportions, same skin "
    "tone and texture, same hair, same eye shape and color, same nose, same "
    "jawline, same stubble pattern. NO identity drift, no morphing, no face "
    "shifting. "
    "MOUTH DISCIPLINE: speaks like a real person on an indoor podcast, not a "
    "theatrical actor. Natural conversational lip movement, SUBTLE lip shapes. "
    "Mouth barely opens for most syllables. Jaw stays nearly closed on soft "
    "consonants. NO exaggerated jaw drop. NO over-articulated speech. NO "
    "shouting. NO mouth-wide-open vowels. Voice is calm controlled "
    "conversational volume, normal speaking energy. "
    "MICRO-MOVEMENT: very subtle head movement, almost still, no exaggerated "
    "nods or tilts, no big head turns. Natural eye blinks every 3-4 seconds. "
    "Hands not visible. No body movement below shoulders. No camera shake. "
    "SEAMLESS CUT POSE: starts the shot with a relaxed neutral expression "
    "and mouth closed, ends the shot with a relaxed neutral expression and "
    "mouth closed (ready for hard cut to next shot). "
    "Studio quiet, no background music in audio, only the spoken Dutch line."
)

SHOTS = [
    {
        "id": 1,
        "ref": "frontal.png",
        "duration": 8,
        "vo": "Overweeg jij AI te implementeren in je MKB, maar weet je niet waar te beginnen? Dan is deze video voor jou.",
        "prompt": (
            "The man in the reference image, exact same identity, speaks "
            "directly to camera in Dutch with calm confident creator-style "
            "delivery. Slight friendly smile starts neutral and warms as the "
            "question lands. Eyebrows raise gently on 'AI' and on 'concreet'. "
            "Energy 7 out of 10, engaging not aggressive."
        ),
    },
    {
        "id": 2,
        "ref": "three_quarter_left.png",
        "duration": 8,
        "vo": "Bij AanloopAI bouwen wij AI-collega's voor MKB'ers in Nederland. Marco belt je leads. Emma handelt je e-mail af.",
        "prompt": (
            "The man in the reference image, exact same identity preserved "
            "from frontal reference, head turned slightly to camera-left at "
            "15 degrees, eyes engaging the lens. On 'AanloopAI' (pronounced "
            "'AAN-loop-ai', three syllables) his head straightens slightly "
            "toward camera as if emphasizing brand name. On 'Marco' and "
            "'Emma' he gestures subtly with eye movement only. Slight smile "
            "throughout."
        ),
    },
    {
        "id": 3,
        "ref": "frontal.png",
        "duration": 8,
        "vo": "En het mooiste? Maakt Marco binnen 3 maanden geen 5 nieuwe afspraken? Dan krijg je elke euro terug.",
        "prompt": (
            "The man in the reference image, exact same identity, frontal "
            "medium close-up. He delivers a key promise. On 'En het mooiste?' "
            "his eyebrows raise sharply (curious playful), confident half-"
            "smile breaks. On 'geen 5 nieuwe afspraken?' voice rises in pitch "
            "as a question. On 'elke euro terug' he leans imperceptibly "
            "toward camera (no zoom) and the smile sharpens into confident "
            "assertion. Energy 8 out of 10, peak emphasis on the guarantee."
        ),
    },
    {
        "id": 4,
        "ref": "three_quarter_right.png",
        "duration": 8,
        "vo": "Samen kijken we naar jouw bedrijf en bouwen we de AI-collega met het hoogste rendement. Onze klanten besparen daardoor tijd op handmatig werk en personeelskosten.",
        "prompt": (
            "The man in the reference image, exact same identity, head turned "
            "slightly to camera-right at 15 degrees. He explains the mechanism "
            "with calm authority. On 'Samen' he tilts head a fraction toward "
            "camera (collaboration cue). On 'hoogste rendement' mild smile of "
            "confidence. On 'tijd op handmatig werk' subtle measured "
            "expression. On 'personeelskosten' confident nod. Energy 7 out of "
            "10, pacing slower at 145 WPM."
        ),
    },
    {
        "id": 5,
        "ref": "frontal.png",
        "duration": 8,
        "vo": "En omdat we Nederland willen veroveren, bieden we tijdelijk een gratis AI-Readiness Scan. Wat krijg je?",
        "prompt": (
            "The man in the reference image, exact same identity, frontal "
            "medium close-up. Direct delivery. On 'Nederland willen "
            "veroveren' confident smile widens (ambition positive). On "
            "'gratis AI-Readiness Scan' (pronounced 'AY-rea-di-ness scan' "
            "clean English loanwords, not over-Dutchified) delivery sharpens, "
            "slight forward intent in posture (no zoom). On 'Wat krijg je?' "
            "eyebrows raise into clean open question, brief held expression "
            "at end of clip for cut. Energy 8 out of 10, offer-reveal peak."
        ),
    },
    {
        "id": 6,
        "ref": "three_quarter_left.png",
        "duration": 8,
        "vo": "Zo werkt Marco voor onze klanten: hij belt 24/7, mist nooit een lead, en zorgt voor meer afspraken in minder tijd.",
        "prompt": (
            "The man in the reference image, exact same identity, head turned "
            "slightly camera-left at 15 degrees, storytelling angle. He "
            "describes Marco's behavior with quiet confidence. On 'Zo werkt "
            "Marco' warm smile of pride. On '24/7' (pronounced "
            "'vierentwintig zeven') subtle head-nod of permanence. On 'mist "
            "nooit een lead' firm slight head shake of certainty. On 'meer "
            "afspraken in minder tijd' confident smile, held final "
            "expression for cut. Energy build 7 to 8 out of 10."
        ),
    },
    {
        "id": 7,
        "ref": "frontal.png",
        "duration": 8,
        "vo": "Dus wil jij ontdekken hoe AI jouw MKB kan laten groeien? Claim nu jouw gratis AI-Readiness Scan.",
        "prompt": (
            "The man in the reference image, exact same identity, frontal "
            "medium close-up. The closer of the ad. On 'Dus wil jij "
            "ontdekken hoe AI' head tilts a fraction toward camera (direct "
            "address). On 'Claim nu' delivery sharpens into clean call-to-"
            "action, slight forward intent in posture (no zoom), confident "
            "smile, eyes locked to camera. Held final beat for transition "
            "to CTA card. Energy 8 to 9 out of 10 on CTA, pacing 130 WPM "
            "slowing on 'Claim nu' for clarity. NOT shouted. Social proof "
            "'4,9 uit 5 sterren' will be added as overlay text in DaVinci, "
            "not spoken here."
        ),
    },
]


def load_ref_image(ref_filename: str):
    from google.genai import types as gtypes
    path = REF_DIR / ref_filename
    if not path.exists():
        raise FileNotFoundError(f"Reference image missing: {path}. Run `make narrator` first.")
    return gtypes.Image(image_bytes=path.read_bytes(), mime_type="image/png")


def generate_shot(client, shot: dict, model: str, force: bool, poll_seconds: int = 15) -> Path:
    from google.genai import types as gtypes

    shot_id = shot["id"]
    out = OUTPUT_DIR / f"shot_{shot_id:02d}.mp4"
    if out.exists() and not force:
        print(f"    [=] Skip (exists): {out.name}")
        return out

    full_prompt = shot["prompt"] + SHARED_VEO_TAIL + f"\n\nSpoken Dutch line: \"{shot['vo']}\""

    print(f"    [+] Shot {shot_id:02d} ({shot['duration']}s, ref={shot['ref']}) — submitting…")
    ref_image = load_ref_image(shot["ref"])

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
            raise TimeoutError(f"Shot {shot_id} polling exceeded 10min — abandon")

    if op.error:
        raise RuntimeError(f"Veo 3 error: {op.error}")
    if not op.result or not op.result.generated_videos:
        raise RuntimeError(f"Veo 3 returned no video (RAI filter? Check op.response)")

    video = op.result.generated_videos[0].video
    if hasattr(video, "video_bytes") and video.video_bytes:
        out.write_bytes(video.video_bytes)
    elif hasattr(video, "uri") and video.uri:
        data = client.files.download(file=video)
        out.write_bytes(data)
    else:
        raise RuntimeError(f"Veo 3 video has no bytes and no URI: {video}")

    print(f"        -> {out}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shot", type=int, help="Generate only this shot (1-7)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Veo model id (default {DEFAULT_MODEL})")
    parser.add_argument("--force", action="store_true", help="Re-generate existing")
    parser.add_argument("--poll", type=int, default=15, help="Poll interval seconds (default 15)")
    args = parser.parse_args()

    key = os.environ.get("GOOGLE_AI_STUDIO_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set in .env")
        sys.exit(1)

    from google import genai
    client = genai.Client(api_key=key)

    selected = [s for s in SHOTS if args.shot is None or s["id"] == args.shot]
    if not selected:
        print(f"[FAIL] Shot {args.shot} not in 1-{len(SHOTS)}")
        sys.exit(1)

    total_sec = sum(s["duration"] for s in selected)
    print(f"Generating {len(selected)} Veo 3 shot(s), total {total_sec}s of video.")
    print(f"Model: {args.model}")
    print(f"Cost note: veo-3.0 in Max plan = $0; preview/lite/3.1 = metered.")
    print()

    failures = []
    for shot in selected:
        try:
            generate_shot(client, shot, args.model, args.force, args.poll)
        except Exception as e:
            print(f"        [FAIL] shot_{shot['id']:02d}: {e}")
            failures.append((shot["id"], str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Veo 3 Konsept R failures\n")
            for sid, msg in failures:
                f.write(f"- shot_{sid:02d}: {msg}\n")
        print(f"\n[WARN] {len(failures)} failures logged to tasks/errors.md")
        sys.exit(1)

    print(f"\n[OK] All {len(selected)} shots generated in {OUTPUT_DIR}")
    print("\nNext: assemble in DaVinci Resolve with grid slides + UI screenshots + jingle.")


if __name__ == "__main__":
    main()

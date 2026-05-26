"""
Google AI Studio Veo 3 ile speaking shot'lari uret.

Brief section 9.2 birebir port + Konsept A 6 speaking-shot (shot 07-12).

Output: assets/video/veo3/<shot>.mp4

Usage:
    python scripts/generate_veo3.py
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/video/veo3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR = Path("prompts/veo3")

SPEAKING_SHOTS = [
    {
        "shot_id":           "shot07_destem",
        "prompt_file":       "shot07_destem.txt",
        "reference_image":   "assets/characters/destem_frontal.png",
        "reference_audio":   "assets/audio/vo/shot07_destem.mp3",
        "duration_seconds":  2.0,
    },
    {
        "shot_id":           "shot08_desecretaresse",
        "prompt_file":       "shot08_desecretaresse.txt",
        "reference_image":   "assets/characters/desecretaresse_frontal.png",
        "reference_audio":   "assets/audio/vo/shot08_desecretaresse.mp3",
        "duration_seconds":  2.0,
    },
    {
        "shot_id":           "shot09a_destemvandesite",
        "prompt_file":       "shot09a_destemvandesite.txt",
        "reference_image":   "assets/characters/destemvandesite_frontal.png",
        "reference_audio":   "assets/audio/vo/shot09a_destemvandesite.mp3",
        "duration_seconds":  2.0,
    },
    {
        "shot_id":           "shot09b_despeurder",
        "prompt_file":       "shot09b_despeurder.txt",
        "reference_image":   "assets/characters/despeurder_frontal.png",
        "reference_audio":   "assets/audio/vo/shot09b_despeurder.mp3",
        "duration_seconds":  2.0,
    },
    {
        "shot_id":           "shot10_deleermeester",
        "prompt_file":       "shot10_deleermeester.txt",
        "reference_image":   "assets/characters/deleermeester_frontal.png",
        "reference_audio":   "assets/audio/vo/shot10_deleermeester.mp3",
        "duration_seconds":  3.0,
    },
    {
        "shot_id":           "shot12_logoreveal",
        "prompt_file":       "shot12_logoreveal.txt",
        "reference_image":   None,
        "reference_audio":   "assets/audio/vo/shot12_anchor_vo.mp3",
        "duration_seconds":  3.0,
    },
]


def generate_shot(shot: dict) -> Path:
    out = OUTPUT_DIR / f"{shot['shot_id']}.mp4"
    if out.exists():
        print(f"    [=] Skip (exists): {out.name}")
        return out

    prompt_path = PROMPTS_DIR / shot["prompt_file"]
    if not prompt_path.exists():
        raise RuntimeError(f"Prompt file missing: {prompt_path}")
    prompt = prompt_path.read_text(encoding="utf-8")

    import google.generativeai as genai

    print(f"    [+] {shot['shot_id']} (duration={shot['duration_seconds']}s)")
    candidates = ["generate_video", "generate_videos", "veo", "Veo"]
    fn = next((getattr(genai, name, None) for name in candidates if getattr(genai, name, None)), None)
    if fn is None:
        raise RuntimeError(
            "Veo 3 entry point not found in google.generativeai. "
            "Run scripts/verify_apis.py and update the candidate list."
        )

    operation = fn(
        model="veo-3.0-generate-preview",
        prompt=prompt,
        config={
            "aspect_ratio":     "9:16",
            "duration_seconds": shot["duration_seconds"],
            "resolution":       "1080p",
            "audio_generation": "enabled",
        },
        reference_image=shot.get("reference_image"),
    )

    while not getattr(operation, "done", False):
        print("        ... generating (Veo 3 ~60-180s)")
        time.sleep(15)
        operation = operation.refresh() if hasattr(operation, "refresh") else operation

    result_video = operation.result.video if hasattr(operation, "result") else operation
    result_video.save(str(out))
    print(f"        -> {out}")
    return out


def main():
    api_key = os.environ.get("GOOGLE_AI_STUDIO_KEY")
    if not api_key:
        print("[FAIL] GOOGLE_AI_STUDIO_KEY not set in .env")
        sys.exit(1)

    import google.generativeai as genai
    genai.configure(api_key=api_key)

    print(f"Generating {len(SPEAKING_SHOTS)} Veo 3 speaking shots\n")
    failures = []
    for shot in SPEAKING_SHOTS:
        try:
            generate_shot(shot)
        except Exception as e:
            print(f"        [FAIL] {shot['shot_id']}: {e}")
            failures.append((shot["shot_id"], str(e)))
            break

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Veo 3 failures\n")
            for sid, msg in failures:
                f.write(f"- {sid}: {msg}\n")
        sys.exit(1)

    print(f"\n[OK] All {len(SPEAKING_SHOTS)} speaking shots in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

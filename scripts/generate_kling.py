"""
Kling AI (API) action / b-roll shot'lari uret.

Kling API: JWT-auth (access_key + secret_key). Free tier kotali; bu proje icin
sufficient. Manuel UI gerekmiyor — script tum 8 dialog-suz shot'u uretir.

Endpoint: https://api.klingai.com/v1/videos/text2video (text-to-video)
          https://api.klingai.com/v1/videos/image2video (image-to-video)

Output: assets/video/kling/<shot>.mp4

Usage:
    python scripts/generate_kling.py
    python scripts/generate_kling.py --only shot01_hook
"""
import os
import sys
import time
import argparse
from pathlib import Path

try:
    import jwt  # PyJWT
    import requests
except ImportError:
    print("[FAIL] Missing deps. Run: pip install PyJWT requests python-dotenv")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()

OUTPUT_DIR = Path("assets/video/kling")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR = Path("prompts/kling")

API_BASE = "https://api.klingai.com"
JWT_ALGORITHM = "HS256"

# 8 dialog-suz action shot (brief section 3.4 storyboard split)
ACTION_SHOTS = [
    {"shot_id": "shot01_hook",         "prompt_file": "shot01_hook.txt",       "duration": 5},
    {"shot_id": "shot02_amplify",      "prompt_file": "shot02_amplify.txt",    "duration": 5},
    {"shot_id": "shot03_signal",       "prompt_file": "shot03_signal.txt",     "duration": 5},
    {"shot_id": "shot04_assemble",     "prompt_file": "shot04_assemble.txt",   "duration": 5},
    {"shot_id": "shot05_entry",        "prompt_file": "shot05_entry.txt",      "duration": 5},
    {"shot_id": "shot06_introwide",    "prompt_file": "shot06_introwide.txt",  "duration": 5},
    {"shot_id": "shot09_split_bg",     "prompt_file": "shot09_split_bg.txt",   "duration": 5},
    {"shot_id": "shot11_resolution",   "prompt_file": "shot11_resolution.txt", "duration": 5},
]


def make_jwt() -> str:
    ak = os.environ.get("KLING_ACCESS_KEY")
    sk = os.environ.get("KLING_SECRET_KEY")
    if not ak or not sk:
        raise RuntimeError("KLING_ACCESS_KEY / KLING_SECRET_KEY not set in .env")
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5,
    }
    return jwt.encode(payload, sk, algorithm=JWT_ALGORITHM, headers={"alg": JWT_ALGORITHM, "typ": "JWT"})


def submit_task(prompt: str, duration: int) -> str:
    token = make_jwt()
    r = requests.post(
        f"{API_BASE}/v1/videos/text2video",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "model_name":   "kling-v1",
            "prompt":       prompt,
            "duration":     str(duration),
            "aspect_ratio": "9:16",
            "mode":         "std",
            "cfg_scale":    0.5,
        },
        timeout=60,
    )
    r.raise_for_status()
    body = r.json()
    if body.get("code") != 0:
        raise RuntimeError(f"Kling submit failed: {body}")
    return body["data"]["task_id"]


def poll_task(task_id: str, timeout_s: int = 600) -> str:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        token = make_jwt()
        r = requests.get(
            f"{API_BASE}/v1/videos/text2video/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        r.raise_for_status()
        body = r.json()
        status = body.get("data", {}).get("task_status")
        if status == "succeed":
            videos = body["data"].get("task_result", {}).get("videos", [])
            if not videos:
                raise RuntimeError(f"Kling task {task_id} succeeded but no video URL")
            return videos[0]["url"]
        if status == "failed":
            raise RuntimeError(f"Kling task {task_id} failed: {body}")
        print(f"        ... status={status}")
        time.sleep(15)
    raise TimeoutError(f"Kling task {task_id} timed out after {timeout_s}s")


def download_video(url: str, out: Path) -> None:
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(out, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 16):
            f.write(chunk)


def generate_shot(shot: dict) -> Path:
    out = OUTPUT_DIR / f"{shot['shot_id']}.mp4"
    if out.exists():
        print(f"    [=] Skip (exists): {out.name}")
        return out

    prompt_path = PROMPTS_DIR / shot["prompt_file"]
    if not prompt_path.exists():
        raise RuntimeError(f"Prompt file missing: {prompt_path}")
    prompt = prompt_path.read_text(encoding="utf-8")

    print(f"    [+] {shot['shot_id']} (duration={shot['duration']}s)")
    task_id = submit_task(prompt, shot["duration"])
    print(f"        task_id={task_id}")
    url = poll_task(task_id)
    download_video(url, out)
    print(f"        -> {out}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="Single shot_id (e.g. shot01_hook)")
    args = parser.parse_args()

    shots = ACTION_SHOTS
    if args.only:
        shots = [s for s in ACTION_SHOTS if s["shot_id"] == args.only]
        if not shots:
            print(f"[FAIL] Unknown shot_id: {args.only}")
            sys.exit(1)

    print(f"Generating {len(shots)} Kling action shots\n")
    failures = []
    for shot in shots:
        try:
            generate_shot(shot)
        except Exception as e:
            print(f"        [FAIL] {shot['shot_id']}: {e}")
            failures.append((shot["shot_id"], str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## Kling AI failures\n")
            for sid, msg in failures:
                f.write(f"- {sid}: {msg}\n")
        print(f"\n[WARN] {len(failures)}/{len(shots)} failed (logged to tasks/errors.md)")
        sys.exit(1 if len(failures) == len(shots) else 0)

    print(f"\n[OK] All {len(shots)} action shots in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

"""
ElevenLabs Music API — continuous bed track for Konsept S ad.

ONE seamless instrumental track that plays under the whole video (intro +
under speech + outro). Consistent mood, no genre switches, no drops.

Output: assets/audio/bed/bed.mp3

Usage:
    python scripts/generate_bed_music.py            # default ~58s
    python scripts/generate_bed_music.py --ms 58000
"""
import argparse
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

OUT = Path("assets/audio/bed/bed.mp3")
OUT.parent.mkdir(parents=True, exist_ok=True)

ENDPOINT = "https://api.elevenlabs.io/v1/music"

PROMPT = (
    "Calm, modern, optimistic corporate technology background music for a "
    "Dutch SME (MKB) AI software advertisement. Soft warm synth pad, gentle "
    "steady electronic pulse, subtle bright piano motif, light airy plucks. "
    "Professional, trustworthy, understated and clean — confident but never "
    "loud or distracting, sits politely under a spoken voice-over. ONE "
    "consistent mood and key from start to finish: NO sudden changes, NO "
    "drops, NO build-ups, NO genre switches, NO vocals, no abrupt section "
    "changes. Steady tempo around 100 BPM, smooth seamless flow, evenly "
    "balanced loudness throughout the entire piece."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ms", type=int, default=58000, help="music length in ms")
    ap.add_argument("--model", default="music_v1")
    args = ap.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        print("[FAIL] ELEVENLABS_API_KEY not set")
        sys.exit(1)

    body = {"prompt": PROMPT, "music_length_ms": args.ms, "model_id": args.model}
    headers = {"xi-api-key": key, "Content-Type": "application/json"}

    print(f"[+] Requesting {args.ms/1000:.0f}s bed from ElevenLabs Music…")
    r = requests.post(ENDPOINT, json=body, headers=headers, timeout=300)

    if r.status_code != 200:
        print(f"[FAIL] HTTP {r.status_code}: {r.text[:500]}")
        sys.exit(2)

    OUT.write_bytes(r.content)
    print(f"[OK] bed written: {OUT} ({len(r.content)/1024:.0f} KB)")


if __name__ == "__main__":
    main()

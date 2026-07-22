"""
Regenerate specific Konsept S shots with multi-key rotation.

Reads Google AI Studio API keys from assets/output/apiler.txt (any format —
keys extracted by regex), uses them BOTTOM-TO-TOP, and advances to the next
key whenever the current one returns 429/RESOURCE_EXHAUSTED. Keys are never
printed (only #index/total), so they stay out of logs.

Reuses SHOTS + generate_shot from generate_veo3_s.py (wide-framing prompt).

Usage:
    python scripts/regen_shots_rotate.py 4 5 6 7
"""
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_veo3_s as g  # noqa: E402
from google import genai  # noqa: E402

KEYS_FILE = Path("assets/output/apiler.txt")
MODEL = "veo-3.1-generate-preview"
INTER_SHOT_SLEEP = 20  # gentle spacing after a success


def load_keys():
    text = KEYS_FILE.read_text(encoding="utf-8", errors="ignore")
    # Google AI Studio keys: legacy "AIza..." and current "AQ.A..." formats.
    found = re.findall(r"(?:AIza[0-9A-Za-z_\-]{20,}|AQ\.[A-Za-z0-9_\-]{30,})", text)
    found = list(reversed(found))  # bottom-to-top
    seen, keys = set(), []
    for k in found:
        if k not in seen:
            seen.add(k)
            keys.append(k)
    return keys


def is_quota_error(msg):
    m = msg.lower()
    return "429" in msg or "resource_exhausted" in m or "quota" in m or "exhausted" in m


def main():
    shot_ids = [int(a) for a in sys.argv[1:]] or [4, 5, 6, 7]
    keys = load_keys()
    if not keys:
        print("[FAIL] no API keys found in apiler.txt")
        sys.exit(1)
    print(f"Loaded {len(keys)} key(s). Regenerating shots: {shot_ids}")

    ki = 0
    for sid in shot_ids:
        shot = next(s for s in g.SHOTS if s["id"] == sid)
        done = False
        while ki < len(keys) and not done:
            try:
                print(f"[shot {sid:02d}] trying key #{ki + 1}/{len(keys)}")
                client = genai.Client(api_key=keys[ki])
                g.generate_shot(client, shot, MODEL, force=True, poll_seconds=15)
                done = True
                time.sleep(INTER_SHOT_SLEEP)
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if is_quota_error(msg):
                    print(f"[shot {sid:02d}] key #{ki + 1} exhausted -> next key")
                else:
                    print(f"[shot {sid:02d}] non-quota error on key #{ki + 1}: {msg[:160]} -> next key")
                ki += 1
        if not done:
            print(f"[FAIL] shot {sid:02d}: all keys exhausted")
            sys.exit(2)

    print("[OK] requested shots regenerated")


if __name__ == "__main__":
    main()

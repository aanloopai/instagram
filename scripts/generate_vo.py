"""
ElevenLabs TTS ile tum shot voiceover'larini uret.

Brief section 9.1 birebir port + Konsept A 12-shot dialog mapping.

Output: assets/audio/vo/shot##_<character>.mp3

Usage:
    python scripts/generate_vo.py
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("assets/audio/vo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOICES = {
    "anchor_vo":       os.environ.get("MARCO_VOICE_ID"),
    "destem":          os.environ.get("MARCO_VOICE_ID"),
    "desecretaresse":  os.environ.get("EMMA_NL_FEMALE_ID"),
    "destemvandesite": os.environ.get("NL_MALE_YOUNG_ID"),
    "despeurder":      os.environ.get("NL_FEMALE_ALTO_ID"),
    "deleermeester":   os.environ.get("NL_MALE_MATURE_ID"),
    "erbil":           os.environ.get("NL_MALE_TIRED_ID"),
}

MODEL = "eleven_multilingual_v2"

SCRIPT = [
    ("shot03",  "erbil",          "Wie...?"),
    ("shot06",  "anchor_vo",      "AanloopAI."),
    ("shot07",  "destem",         "Goedendag, met Alfa Reclame. Waarmee kan ik u helpen?"),
    ("shot08",  "desecretaresse", "Drie afspraken ingepland. Niets vergeten."),
    ("shot09a", "destemvandesite", "24/7 op je website."),
    ("shot09b", "despeurder",     "Vijftien nieuwe leads. Vanavond."),
    ("shot10",  "deleermeester",  "En wij leren het je. Stap voor stap."),
    ("shot12",  "anchor_vo",      "AanloopAI. Voor het MKB van morgen."),
]


def generate_vo(shot: str, character: str, text: str, client) -> Path:
    out = OUTPUT_DIR / f"{shot}_{character}.mp3"
    if out.exists():
        print(f"    [=] Skip (exists): {out.name}")
        return out

    voice_id = VOICES.get(character)
    if not voice_id:
        raise RuntimeError(f"No voice ID configured for character '{character}'. Check .env")

    print(f"    [+] {shot} - {character}: {text!r}")
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=MODEL,
        output_format="mp3_44100_192",
        voice_settings={
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.30,
            "use_speaker_boost": True,
        },
    )
    with open(out, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    print(f"        -> {out}")
    return out


def main():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("[FAIL] ELEVENLABS_API_KEY not set in .env")
        sys.exit(1)

    missing = [c for c in VOICES if not VOICES[c]]
    if missing:
        print(f"[FAIL] Missing voice IDs in .env for: {', '.join(missing)}")
        print("       Run scripts/verify_apis.py to scan NL voices, then update .env")
        sys.exit(1)

    from elevenlabs.client import ElevenLabs
    client = ElevenLabs(api_key=api_key)

    print(f"Generating {len(SCRIPT)} voiceovers\n")
    failures = []
    for shot, character, text in SCRIPT:
        try:
            generate_vo(shot, character, text, client)
        except Exception as e:
            print(f"        [FAIL] {shot}_{character}: {e}")
            failures.append((shot, character, str(e)))

    if failures:
        Path("tasks").mkdir(exist_ok=True)
        with open("tasks/errors.md", "a", encoding="utf-8") as f:
            f.write("\n## ElevenLabs VO failures\n")
            for s, c, msg in failures:
                f.write(f"- {s}_{c}: {msg}\n")
        sys.exit(1)

    print(f"\n[OK] All {len(SCRIPT)} voiceovers in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

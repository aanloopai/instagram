"""
API surface verification before running the production pipeline.

Brief v2.0 notu: Google API hizli evrildigi icin Veo 3 + Imagen 4 method
adlari her sprint dogrulanmali. Bu script `dir(genai)` ile actual surface
check yapar + ElevenLabs Voice Library'den NL voice listesi cikarir.

Usage:
    python scripts/verify_apis.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def check_google_genai():
    print("\n[1/2] Google AI Studio (google-generativeai)")
    print("-" * 60)
    try:
        import google.generativeai as genai
    except ImportError:
        print("    [FAIL] google-generativeai not installed.")
        print("    Run: pip install google-generativeai")
        return False

    key = os.environ.get("GOOGLE_AI_STUDIO_KEY")
    if not key:
        print("    [FAIL] GOOGLE_AI_STUDIO_KEY not set in .env")
        return False

    genai.configure(api_key=key)

    surface = [name for name in dir(genai) if not name.startswith("_")]
    video_candidates = [n for n in surface if "video" in n.lower() or "veo" in n.lower()]
    image_candidates = [n for n in surface if "image" in n.lower() or "imagen" in n.lower()]

    print(f"    Top-level surface ({len(surface)} items): {', '.join(surface[:8])}...")
    print(f"    Video-related: {video_candidates or 'NONE (Veo 3 may need separate vertex-ai client)'}")
    print(f"    Image-related: {image_candidates or 'NONE (Imagen may need separate vertex-ai client)'}")

    try:
        models = list(genai.list_models())
        veo = [m.name for m in models if "veo" in m.name.lower()]
        imagen = [m.name for m in models if "imagen" in m.name.lower()]
        print(f"    Veo models available: {veo or 'NONE - check Vertex AI access'}")
        print(f"    Imagen models available: {imagen or 'NONE - check Vertex AI access'}")
        return True
    except Exception as e:
        print(f"    [WARN] list_models failed: {e}")
        return False


def check_elevenlabs():
    print("\n[2/2] ElevenLabs API")
    print("-" * 60)
    try:
        from elevenlabs.client import ElevenLabs
    except ImportError:
        print("    [FAIL] elevenlabs not installed.")
        print("    Run: pip install elevenlabs")
        return False

    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        print("    [FAIL] ELEVENLABS_API_KEY not set in .env")
        return False

    try:
        client = ElevenLabs(api_key=key)
        voices = client.voices.get_all()
        all_voices = voices.voices if hasattr(voices, "voices") else voices
        print(f"    Total voices accessible: {len(all_voices)}")

        nl_voices = []
        for v in all_voices:
            labels = getattr(v, "labels", {}) or {}
            language = (labels.get("language") or "").lower()
            description = (getattr(v, "description", "") or "").lower()
            if "dutch" in language or "nl" in language or "dutch" in description:
                nl_voices.append((v.voice_id, v.name, labels))

        print(f"    Dutch-tagged voices: {len(nl_voices)}")
        for vid, name, labels in nl_voices[:10]:
            gender = labels.get("gender", "?") if isinstance(labels, dict) else "?"
            print(f"      {vid[:24]}...  {name:24}  gender={gender}")
        if not nl_voices:
            print("    [WARN] No NL voices. Use Voice Lab clone or eleven_multilingual_v2 model.")
        return True
    except Exception as e:
        print(f"    [FAIL] ElevenLabs API call failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("AanloopAI Reklam - API Surface Verification")
    print("=" * 60)
    ok_google = check_google_genai()
    ok_eleven = check_elevenlabs()
    print("\n" + "=" * 60)
    print(f"Google AI Studio: {'OK' if ok_google else 'FAIL'}")
    print(f"ElevenLabs:       {'OK' if ok_eleven else 'FAIL'}")
    print("=" * 60)
    sys.exit(0 if (ok_google and ok_eleven) else 1)

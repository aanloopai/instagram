"""
Generate timeline-aligned SRT for Konsept S via Groq Whisper.

Per shot:
  1. ffmpeg extract audio (mono 16kHz wav)
  2. Groq Whisper API (whisper-large-v3, word-level granularity, lang=nl)
  3. Format word groups into SRT cues (max 4 words per cue, ~1.5s each)

Final: merge all 7 SRTs into single timeline with shot offsets.

Output: assets/subtitles/konsept_s.srt

Usage:
    python scripts/generate_subtitles.py             # all 7 shots
    python scripts/generate_subtitles.py --shot 1    # one shot
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
WATCH_ENV = Path.home() / ".config" / "watch" / ".env"
if WATCH_ENV.exists():
    for line in WATCH_ENV.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

VIDEO_DIR = Path("assets/video/konsept_s/veo3")
SUB_DIR = Path("assets/subtitles")
SUB_DIR.mkdir(parents=True, exist_ok=True)

SHOTS = [
    (1, 0),
    (2, 8),
    (3, 16),
    (4, 24),
    (5, 32),
    (6, 40),
    (7, 48),
]


def find_ffmpeg() -> str:
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    candidates = list(Path("C:/Users/Hallo/AppData/Local/Microsoft/WinGet/Packages").glob(
        "Gyan.FFmpeg_*/ffmpeg-*-full_build/bin/ffmpeg.exe"))
    if candidates:
        return str(candidates[0])
    raise RuntimeError("ffmpeg not found. Install via winget Gyan.FFmpeg.")


def extract_audio(ffmpeg: str, video: Path, work: Path) -> Path:
    out = work / "audio.wav"
    subprocess.run([
        ffmpeg, "-y", "-v", "error", "-i", str(video),
        "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k",
        str(out),
    ], check=True)
    return out


def transcribe(audio: Path) -> dict:
    from groq import Groq
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY not set. Add to ~/.config/watch/.env or repo .env.")
    client = Groq(api_key=key)
    with audio.open("rb") as f:
        return client.audio.transcriptions.create(
            file=(audio.name, f.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
            timestamp_granularities=["word"],
            language="nl",
        ).model_dump()


def fmt_srt_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds * 1000) % 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def group_words_into_cues(words: list, max_words: int = 4, max_gap: float = 0.5):
    cues = []
    current = []
    for w in words:
        text = w.get("word") or w.get("text") or ""
        start = w.get("start", 0)
        end = w.get("end", start)
        if current and (
            len(current) >= max_words
            or (start - current[-1]["end"]) > max_gap
            or text.endswith((".", "!", "?"))
        ):
            cues.append({
                "start": current[0]["start"],
                "end": current[-1]["end"],
                "text": " ".join(c["text"] for c in current).strip(),
            })
            if text.endswith((".", "!", "?")) and len(current) < max_words:
                current.append({"text": text.strip(), "start": start, "end": end})
                cues[-1]["end"] = end
                cues[-1]["text"] = " ".join(c["text"] for c in current).strip()
                current = []
                continue
            current = []
        current.append({"text": text.strip(), "start": start, "end": end})
    if current:
        cues.append({
            "start": current[0]["start"],
            "end": current[-1]["end"],
            "text": " ".join(c["text"] for c in current).strip(),
        })
    return cues


def write_shot_srt(shot_id: int, cues: list, offset: float) -> Path:
    out = SUB_DIR / f"shot_{shot_id:02d}.srt"
    lines = []
    for i, cue in enumerate(cues, 1):
        lines.append(str(i))
        lines.append(f"{fmt_srt_time(cue['start'] + offset)} --> {fmt_srt_time(cue['end'] + offset)}")
        lines.append(cue["text"])
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def write_master_srt(all_cues: list) -> Path:
    out = SUB_DIR / "konsept_s.srt"
    lines = []
    for i, cue in enumerate(all_cues, 1):
        lines.append(str(i))
        lines.append(f"{fmt_srt_time(cue['start'])} --> {fmt_srt_time(cue['end'])}")
        lines.append(cue["text"])
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def process_shot(ffmpeg: str, shot_id: int, offset: float) -> list:
    video = VIDEO_DIR / f"shot_{shot_id:02d}.mp4"
    if not video.exists():
        print(f"    [SKIP] {video} not found")
        return []
    print(f"    [+] Shot {shot_id:02d} (offset={offset}s)")
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        audio = extract_audio(ffmpeg, video, work)
        result = transcribe(audio)
    words = result.get("words", [])
    if not words:
        segments = result.get("segments", [])
        words = []
        for seg in segments:
            for word_data in (seg.get("words") or []):
                words.append(word_data)
    cues = group_words_into_cues(words)
    write_shot_srt(shot_id, cues, offset)
    print(f"        cues: {len(cues)}")
    return [
        {"start": c["start"] + offset, "end": c["end"] + offset, "text": c["text"]}
        for c in cues
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shot", type=int, help="Process only this shot")
    args = parser.parse_args()

    ffmpeg = find_ffmpeg()
    selected = SHOTS if args.shot is None else [(args.shot, next(o for s, o in SHOTS if s == args.shot))]

    all_cues = []
    for sid, offset in selected:
        try:
            cues = process_shot(ffmpeg, sid, offset)
            all_cues.extend(cues)
        except Exception as e:
            print(f"    [FAIL] shot_{sid:02d}: {e}")

    if args.shot is None and all_cues:
        master = write_master_srt(all_cues)
        print(f"\n[OK] Master SRT: {master} ({len(all_cues)} cues)")


if __name__ == "__main__":
    main()

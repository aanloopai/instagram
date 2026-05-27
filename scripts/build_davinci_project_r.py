"""
Konsept R timeline manifest + DaVinci assembly guide writer.

Emits:
  assets/timeline_konsept_r_manifest.json — machine-readable cut list
  docs/DAVINCI_ASSEMBLY_R.md              — step-by-step manual guide
  scripts/concat_preview.sh               — quick ffmpeg concat (no overlays)

FCPXML generation skipped (brittle to hand-write; user imports manually via
the manifest + guide).

Usage:
    python scripts/build_davinci_project_r.py
"""
import json
from pathlib import Path

TIMELINE = [
    ("V1", "shot_01",            0.0,  8.0,  "assets/video/konsept_r/veo3/shot_01.mp4",
        "Hook + bridge — 'Overweeg jij AI te implementeren...'"),
    ("V1", "shot_02",            8.0, 16.0,  "assets/video/konsept_r/veo3/shot_02.mp4",
        "Brand reveal — 'Bij AanloopAI bouwen wij AI-collega's...'"),
    ("V1", "shot_03",           16.0, 24.0,  "assets/video/konsept_r/veo3/shot_03.mp4",
        "Guarantee tease — 'En het mooiste? ...elke euro terug.'"),
    ("V1", "shot_04",           26.0, 34.0,  "assets/video/konsept_r/veo3/shot_04.mp4",
        "Mechanism — 'Samen kijken we... tijd op handmatig werk...'"),
    ("V1", "shot_05",           34.0, 42.0,  "assets/video/konsept_r/veo3/shot_05.mp4",
        "Offer reveal — 'gratis AI-Readiness Scan. Wat krijg je?'"),
    ("V1", "shot_06",           46.0, 54.0,  "assets/video/konsept_r/veo3/shot_06.mp4",
        "Marco behavior — '24/7, mist nooit een lead...'"),
    ("V1", "shot_07",           54.0, 62.0,  "assets/video/konsept_r/veo3/shot_07.mp4",
        "CTA bridge — 'Claim nu jouw gratis AI-Readiness Scan.'"),
    ("V2", "slide_01_risk",     24.0, 26.0,  "assets/slides/slide_01_risk_reversal.png",
        "INSERT: 'Dan krijg je elke euro terug.' (blue)"),
    ("V2", "slide_02_eerste20", 42.0, 44.0,  "assets/slides/slide_02_eerste_20.png",
        "INSERT: 'De eerste 20 MKB'ers' + buildings"),
    ("V2", "slide_03_kansen",   44.0, 46.0,  "assets/slides/slide_03_drie_kansen.png",
        "INSERT: 'drie grootste AI-kansen' + EUR"),
    ("V2", "slide_04_urgency",  53.0, 54.0,  "assets/slides/slide_04_urgency.png",
        "INSERT: 'Wees er snel bij' (red, 1s only)"),
    ("V2", "slide_05_cta_card", 62.0, 66.0,  "assets/slides/slide_05_cta_card.png",
        "FINAL CTA CARD hold 4s"),
    ("V3", "ui_marco",          10.0, 12.0,  "assets/ui/mockup_01_marco_dashboard.png",
        "Marco dashboard float, 12deg tilt right, soft shadow, scale 0.7"),
    ("V3", "ui_emma",           13.0, 15.0,  "assets/ui/mockup_02_emma_chat.png",
        "Emma chat float, 12deg tilt left, soft shadow, scale 0.7"),
    ("V3", "ui_readiness",      37.0, 39.0,  "assets/ui/mockup_03_ai_readiness.png",
        "AI-Readiness landing float, 8deg tilt right, scale 0.65"),
    ("V3", "logo_bug",           8.0, 62.0,  "assets/logo/aanloopai-bug.png",
        "Persistent 200x60 top-left bug logo (semi-transparent)"),
    ("V4", "subtitles",          0.0, 62.0,  "assets/subtitles/konsept_r.srt",
        "Burn-in NL subtitle, 1 phrase/time, white outline + drop shadow"),
    ("A2", "jingle_intro",       0.0,  1.8,  "assets/audio/jingle/intro.wav",
        "Forte abrupt cut at t=0 (-6dB hit)"),
    ("A2", "jingle_outro",      62.0, 66.0,  "assets/audio/jingle/outro.wav",
        "Sustained + synth swell, fades over CTA card"),
    ("A3", "bed_music",          0.0, 66.0,  "assets/audio/bed/underscore_25s.wav",
        "Loop 25s clip 3x to fill 66s, sidechain compressor key A1 VO"),
]

EFFECTS = [
    ("V1+V2+V3", "Color Grade — oxblood backdrop boost + warm bone overlay (DaVinci Color page)"),
    ("V1+V2+V3", "Sharpen — Unsharp Mask amount=0.4, radius=1.2 (subtle, Veo 720p netlik boost)"),
    ("V1+V2+V3", "Film Grain — subtle DaVinci OFX Grain @ 35mm 200ASA, opacity 18%"),
    ("V1+V2+V3", "Chromatic Aberration — DaVinci OFX, amount 0.2px (cinematic feel)"),
    ("A1",       "EQ HPF 200Hz + presence +3dB @ 3kHz"),
    ("A1",       "Compressor 3:1, threshold -18dB"),
    ("A3",       "Sidechain Compressor — key A1 VO, ratio 4:1, threshold -22dB"),
    ("A3",       "EQ — 1-4 kHz dip -4dB (VO pocket)"),
    ("Master",   "Bus Compressor 2:1"),
    ("Master",   "Normalize to -14 LUFS"),
    ("Master",   "True-peak limiter -1 dBFS"),
]

TOPAZ_PIPELINE = [
    "Step 1: import all 7 shot_##.mp4 to Topaz Video AI 6",
    "Step 2: apply Proteus v4 model — Settings: Enhance Detail 35, Recover Detail 25, "
    "        Sharpen 15, Reduce Noise 18, Anti-Alias 20",
    "Step 3: upscale 720x1280 -> 2160x3840 (4K vertical), then downscale 1080x1920 in DaVinci",
    "Step 4: export as ProRes 422 HQ (.mov) -> assets/video/konsept_r/topaz/",
    "Step 5: import Topaz outputs into DaVinci V1 (replace original Veo shots)",
]


def write_manifest():
    out = Path("assets/timeline_konsept_r_manifest.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "format": "9:16 1080x1920 24fps H.264",
        "duration_s": 66.0,
        "audio_target": "-14 LUFS, -1 dBFS peak",
        "tracks": [
            {
                "track": t, "label": lbl, "start_s": s, "end_s": e,
                "duration_s": round(e - s, 2), "source": src, "notes": notes,
            }
            for t, lbl, s, e, src, notes in TIMELINE
        ],
        "effects": [{"target": tgt, "spec": spec} for tgt, spec in EFFECTS],
        "topaz_pre_pipeline": TOPAZ_PIPELINE,
    }
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[OK] Manifest: {out}")
    return data


def write_assembly_guide(data: dict):
    out = Path("docs/DAVINCI_ASSEMBLY_R.md")
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# DaVinci Resolve assembly guide — Konsept R",
        "",
        "**Target**: 9:16 1080x1920 24fps H.264, 66s total, -14 LUFS audio",
        "**Source manifest**: `assets/timeline_konsept_r_manifest.json`",
        "",
        "## 0. Pre-process — Topaz Video AI (ZORUNLU realism boost)",
        "",
    ]
    for step in TOPAZ_PIPELINE:
        lines.append(f"- {step}")

    lines += [
        "",
        "## 1. New project",
        "",
        "- File > New Project: `aanloopai_konsept_r`",
        "- File > Project Settings:",
        "  - Resolution: 1080 x 1920 (vertical)",
        "  - Frame rate: 24 fps",
        "  - Color science: DaVinci YRGB Color Managed",
        "",
        "## 2. Import media",
        "",
        "- Media Pool > Import:",
        "  - 7 Topaz-cleaned MP4s (or original Veo if Topaz skipped)",
        "  - 5 slide PNGs from `assets/slides/`",
        "  - 3 UI mockup PNGs from `assets/ui/`",
        "  - `assets/logo/aanloopai-bug.png`",
        "  - Suno WAVs from `assets/audio/jingle/` + `assets/audio/bed/`",
        "",
        "## 3. Timeline placements",
        "",
        "Tracks (top to bottom):",
        "- **V4** subtitle layer (Fairlight Subtitles, burn at export)",
        "- **V3** floating overlays + logo bug",
        "- **V2** grid slide inserts (full-frame replace V1)",
        "- **V1** Veo talking-head spine",
        "- **A1** Veo embedded VO",
        "- **A2** Suno jingle hits",
        "- **A3** Suno bed music",
        "",
        "Per-cut placements:",
        "",
        "| Track | Label | Start | End | Source | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for track in data["tracks"]:
        lines.append(
            f"| {track['track']} | {track['label']} | "
            f"{track['start_s']:.1f}s | {track['end_s']:.1f}s | "
            f"`{track['source']}` | {track['notes']} |"
        )

    lines += [
        "",
        "## 4. Effects + grading",
        "",
        "| Target | Effect spec |",
        "|---|---|",
    ]
    for eff in data["effects"]:
        lines.append(f"| {eff['target']} | {eff['spec']} |")

    lines += [
        "",
        "## 5. Subtitle generation",
        "",
        "Use Veo embedded audio + Whisper to generate per-shot SRT:",
        "",
        "```bash",
        "for shot in assets/video/konsept_r/veo3/shot_*.mp4; do",
        "  whisper --model medium --language nl --output_format srt \"$shot\" \\",
        "    --output_dir assets/subtitles/",
        "done",
        "",
        "# Merge all 7 SRTs into single timeline-aligned konsept_r.srt",
        "python scripts/merge_subtitles.py  # TODO: implement",
        "```",
        "",
        "Alternative: re-use Groq Whisper from `~/.config/watch/.env`",
        "(see `scripts/watch.py` pattern).",
        "",
        "## 6. Export master",
        "",
        "- Deliver page:",
        "  - Format: MP4",
        "  - Codec: H.264",
        "  - Resolution: 1080 x 1920",
        "  - Frame rate: 24 fps",
        "  - Bitrate: 25 Mbps",
        "  - Audio: AAC 320 kbps stereo",
        "  - Loudness: -14 LUFS integrated, -1 dBFS true peak",
        "- Output: `assets/output/konsept_r_master_66s.mp4`",
        "",
        "## 7. Variant cuts (after master)",
        "",
        "- **30s mid-form**: trim per spec section 5",
        "- **9s Stories cut**: trim per spec section 5",
        "",
        "## 8. QA checklist (yayindan once)",
        "",
        "Per spec section 6:",
        "- [ ] Hook 1.0s blind test 5-kisi (%80+ \"stop scroll\")",
        "- [ ] Lip-sync %95+ frame-by-frame",
        "- [ ] NL accent + telaffuz native check",
        "- [ ] aanloopai logo min 3x gorsel + sozlu",
        "- [ ] CTA UTM `?utm_source=meta&utm_campaign=konseptR&utm_content=v1`",
        "- [ ] Meta Pixel event `AI_Readiness_Scan_Claim`",
        "- [ ] Landing match `aanloopai.nl/ai-readiness-scan` ile copy 1:1",
        "- [ ] Audio caption-sound-off test (subtitle olmadan anlasilir mi?)",
        "- [ ] 9:16 1080x1920 24fps H.264 25Mbps",
        "- [ ] -14 LUFS, -1 dBFS peak",
        "",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Guide: {out}")


def write_concat_preview():
    out = Path("scripts/concat_preview.sh")
    out.parent.mkdir(parents=True, exist_ok=True)
    script = (
        "#!/usr/bin/env bash\n"
        "# Quick ffmpeg concat of 7 Veo talking-head shots for raw preview.\n"
        "# No slides, no overlays, no grade — pure spine + embedded VO.\n"
        "# Output: assets/output/konsept_r_concat_preview.mp4\n"
        "set -euo pipefail\n"
        "\n"
        "# Find ffmpeg (winget Gyan.FFmpeg default install path on Windows)\n"
        "if ! command -v ffmpeg >/dev/null 2>&1; then\n"
        "  FFMPEG_BIN=$(ls -d /c/Users/*/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_*/ffmpeg-*-full_build/bin 2>/dev/null | head -1)\n"
        "  if [ -n \"$FFMPEG_BIN\" ]; then\n"
        "    export PATH=\"$FFMPEG_BIN:$PATH\"\n"
        "  else\n"
        "    echo 'ffmpeg not found — install via: winget install Gyan.FFmpeg'\n"
        "    exit 1\n"
        "  fi\n"
        "fi\n"
        "\n"
        "OUT_DIR=assets/output\n"
        "mkdir -p \"$OUT_DIR\"\n"
        "\n"
        "LIST=$(mktemp --suffix=.txt)\n"
        "PROJ_WIN=$(cygpath -w \"$(pwd)\" 2>/dev/null || pwd)\n"
        "for i in 01 02 03 04 05 06 07; do\n"
        "  PATH_WIN=$(cygpath -w \"$(pwd)/assets/video/konsept_r/veo3/shot_$i.mp4\" 2>/dev/null || echo \"assets/video/konsept_r/veo3/shot_$i.mp4\")\n"
        "  echo \"file '${PATH_WIN//\\\\/\\\\\\\\}'\" >> \"$LIST\"\n"
        "done\n"
        "\n"
        "ffmpeg -y -f concat -safe 0 -i \"$LIST\" -c copy \"$OUT_DIR/konsept_r_concat_preview.mp4\"\n"
        "echo \"-> $OUT_DIR/konsept_r_concat_preview.mp4\"\n"
        "rm -f \"$LIST\"\n"
    )
    out.write_text(script, encoding="utf-8")
    out.chmod(0o755)
    print(f"[OK] Concat preview: {out}")


def main():
    data = write_manifest()
    write_assembly_guide(data)
    write_concat_preview()
    print(f"\nTotal timeline: 66.0s")
    print(f"Tracks: {len(data['tracks'])} cuts")
    print(f"Effects: {len(data['effects'])} entries")
    print(f"\nNext:")
    print(f"  1. Buy + run Topaz Video AI on shots (see topaz_pre_pipeline)")
    print(f"  2. Open DaVinci Resolve > follow docs/DAVINCI_ASSEMBLY_R.md")
    print(f"  3. Or quick preview: bash scripts/concat_preview.sh")


if __name__ == "__main__":
    main()

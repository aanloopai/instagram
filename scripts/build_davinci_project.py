"""
DaVinci Resolve FCP XML project dosyasi uret (Fase 3 placeholder).

Plan: Tum shot'lari timeline'a yerlestir, audio sync noktalarini hizala,
logo overlay marker'larini koy. DaVinci Resolve free .fcpxml import destekler.

Output: assets/timeline.fcpxml + assets/timeline_manifest.json

Status: STUB - Fase 3 baslayinca implement edilecek. Su anda sadece
shot inventory + timeline manifest yazar.

Usage:
    python scripts/build_davinci_project.py
"""
import json
from pathlib import Path

# Brief section 3.4 storyboard - 12 shot, 0-25 sn
TIMELINE = [
    # (shot_id, start_s, end_s, source_file, vo_file, notes)
    ("shot01_hook",            0.0,  1.0,  "assets/video/kling/shot01_hook.mp4",            None,                                       "23 missed call + yagmur"),
    ("shot02_amplify",         1.0,  3.0,  "assets/video/kling/shot02_amplify.mp4",         None,                                       "4 cut, heartbeat 60bpm"),
    ("shot03_signal",          3.0,  5.0,  "assets/video/kling/shot03_signal.mp4",          "assets/audio/vo/shot03_erbil.mp3",         "Rotterdam skyline sky-projection logo"),
    ("shot04_assemble",        5.0,  7.0,  "assets/video/kling/shot04_assemble.mp4",        None,                                       "5 silhouette 0.4s each + jingle Aan!"),
    ("shot05_entry",           7.0,  9.0,  "assets/video/kling/shot05_entry.mp4",           None,                                       "Ofis kapisi patlama, ...loop!"),
    ("shot06_introwide",       9.0, 11.0,  "assets/video/kling/shot06_introwide.mp4",       "assets/audio/vo/shot06_anchor_vo.mp3",     "5 kahraman tam cerceve, ...AI! + bug logo basla"),
    ("shot07_destem",         11.0, 13.0,  "assets/video/veo3/shot07_destem.mp4",           "assets/audio/vo/shot07_destem.mp3",        "De Stem telefon kapma"),
    ("shot08_desecretaresse", 13.0, 15.0,  "assets/video/veo3/shot08_desecretaresse.mp4",   "assets/audio/vo/shot08_desecretaresse.mp3", "E-mail -> Calendar"),
    ("shot09_split",          15.0, 17.0,  "assets/video/kling/shot09_split_bg.mp4",        "assets/audio/vo/shot09a+shot09b",          "Split screen chat + LinkedIn"),
    ("shot10_deleermeester",  17.0, 19.0,  "assets/video/veo3/shot10_deleermeester.mp4",    "assets/audio/vo/shot10_deleermeester.mp3", "Mentor omuz dokunusu"),
    ("shot11_resolution",     19.0, 22.0,  "assets/video/kling/shot11_resolution.mp4",      None,                                       "Erbil gun isiginda, koro fisilti AanloopAI"),
    ("shot12_logoreveal",     22.0, 25.0,  "assets/video/veo3/shot12_logoreveal.mp4",       "assets/audio/vo/shot12_anchor_vo.mp3",     "CTA + jingle resolve"),
]


def write_manifest():
    out = Path("assets/timeline_manifest.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    data = [
        {
            "shot_id":   sid,
            "start_s":   start,
            "end_s":     end,
            "duration":  round(end - start, 2),
            "video":     vid,
            "vo":        vo,
            "notes":     notes,
        }
        for sid, start, end, vid, vo, notes in TIMELINE
    ]
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[OK] Manifest yazildi: {out} ({len(data)} shots, {data[-1]['end_s']}s total)")


def write_stub_fcpxml():
    out = Path("assets/timeline.fcpxml")
    stub = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- STUB: Fase 3 baslayinca pyfcpxml veya manuel template ile genislet -->\n'
        '<!-- Bkz: assets/timeline_manifest.json shot listesi icin -->\n'
        '<fcpxml version="1.10">\n'
        '  <resources/>\n'
        '  <library/>\n'
        '</fcpxml>\n'
    )
    out.write_text(stub, encoding="utf-8")
    print(f"[STUB] FCP XML placeholder: {out}")


if __name__ == "__main__":
    write_manifest()
    write_stub_fcpxml()
    print("\nFase 3 baslayinca:")
    print("  1. DaVinci Resolve free yukle")
    print("  2. assets/timeline_manifest.json oku, .fcpxml'i pyfcpxml ile uret")
    print("  3. DaVinci > File > Import > Timeline > .fcpxml")

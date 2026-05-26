# CLAUDE.md — aanloopai-reklam

Project handoff icin Claude Code workflow notlari.

## Genel

- **Proje**: AanloopAI Instagram Reklam (Konsept A — "De Reddingsbrigade").
- **Brief**: `C:\Users\Hallo\Desktop\aanloopai_instagram_reklam_brief_v2.md` (v2.0, 26 Mei 2026).
- **Plan**: `C:\Users\Hallo\.claude\plans\lexical-giggling-token.md` (M tarafindan onaylandi).
- **Stack**: Google AI Studio (Imagen 4 + Veo 3) + Kling AI free + ElevenLabs API + Suno Pro + DaVinci Resolve.
- **Toplam ek maliyet**: $10/ay (Suno Pro).
- **Hedef cikti**: 25 sn 9:16 Reels master + 9 sn Stories cut.

## Workflow

- Global CLAUDE.md kurallari aktif (TURKCE strict, caveman full intensity, Eisenhower Q1-Q4, otonom 4u sessiyon).
- Brief Konsept A primary. Konsept B/C DEFER (Wave-2 sonrasi).
- Speaking shot Veo 3, dialog-suz Kling (credit ekonomi).
- Logo ASLA AI ile uretilmez — `assets/logo/aanloopai.svg` overlay.
- Cinsiyet-ses esleme zorunlu (brief section 3.3): kadin karakter <-> kadin TTS.

## Faseler

| # | Ad | Sure | Trigger |
|---|---|---|---|
| 0 | Setup | ~2h | `make characters` calismadan once tamam olmali |
| 1 | Pre-production | ~4h | Imagen + ElevenLabs + Suno |
| 2 | Production | ~1g | Veo 3 + Kling generate |
| 3 | Post | ~1g | DaVinci Resolve assemble |
| 4 | Variants | ~2h | Stories cut + B/C defer |
| 5 | Launch | ~1g | Meta Ads + 48h review |

Detay: `tasks/todo.md`.

## Pipeline

```bash
cp .env.example .env  # ELEVENLABS_API_KEY + GOOGLE_AI_STUDIO_KEY doldur
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install google-generativeai elevenlabs python-dotenv

make verify        # API surface dogrulamasi
make characters    # Imagen 4 portreleri (15 dosya)
make vo            # ElevenLabs VO (8 MP3)
make video         # Veo 3 speaking shots (6 MP4)
make kling         # Kling AI API: 8 action / b-roll shots
# Manuel: Suno Pro jingle (web UI — Suno resmi API yok)
make assemble      # DaVinci timeline build
```

## QA checklist (yayindan once)

`tasks/lessons.md` ve brief section 12 referansli. Ozet:

- AanloopAI 3x sozlu + 3x gorsel.
- Lip-sync %95+.
- 9:16 1080x1920 24fps H.264 25Mbps.
- Audio -14 LUFS, -1 dBFS peak.
- Hook 1.0 sn icinde "stop scroll" (5-kisi blind test).

## Hata logu

`tasks/errors.md` otomatik olusur. Veo 3 API method degisirse `scripts/verify_apis.py` re-run.

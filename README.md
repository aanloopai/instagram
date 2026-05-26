# aanloopai-reklam

AanloopAI Instagram Reklam — Konsept A "De Reddingsbrigade".

5 super-kahraman / 5 AI urun, 25 sn Reels master + 9 sn Stories cut. Google AI Studio stack (Imagen 4 + Veo 3) + Kling AI free + ElevenLabs + Suno Pro + DaVinci Resolve.

## Hizli baslangic

```bash
# 1. Setup
cp .env.example .env
# .env doldur: ELEVENLABS_API_KEY, GOOGLE_AI_STUDIO_KEY

python -m venv .venv
.venv\Scripts\activate           # Windows
pip install google-generativeai elevenlabs python-dotenv PyJWT requests

# 2. API surface dogrula (Google API hizli evrildigi icin)
python scripts/verify_apis.py

# 3. Asset pipeline
make characters       # Imagen 4: 5 char x 3 angle = 15 portre
make vo               # ElevenLabs: 8 NL VO mp3
make video            # Veo 3: 6 speaking shot
make kling            # Kling AI API: 8 action / b-roll shot
# Manuel: Suno Pro jingle (UI, prompts/suno/jingle.txt — Suno API yok)

# 4. Post
make assemble         # DaVinci FCP XML build
```

## Yapi

- `tasks/todo.md` — 6 fase, 45+ checkbox (ana yol haritasi).
- `tasks/lessons.md` — 11 onceden uyari (lip-sync, hook rate, IP, vb).
- `scripts/` — 5 Python pipeline script.
- `prompts/` — Imagen + Veo 3 + Kling + Suno prompt templates (8+ dosya).
- `assets/` — output (gitignored haric `assets/logo/`).

## Onemli kurallar

- Logo ASLA AI ile uretilmez. `assets/logo/aanloopai.svg` overlay kullanilir.
- Speaking shot <= 4 sn, <= 1 cumle (lip-sync icin).
- Ses ONCE, video SONRA. ElevenLabs -> Veo 3.
- Cinsiyet-ses esleme zorunlu (brief section 3.3).
- "aanloopai" min 3x sozlu + 3x gorsel (brief section 12 QA).

## Reference

- Brief: `C:\Users\Hallo\Desktop\aanloopai_instagram_reklam_brief_v2.md`
- Plan: `C:\Users\Hallo\.claude\plans\lexical-giggling-token.md`
- Aanloop ana repo: `C:\Users\Hallo\OneDrive\Claude\AGA\aanloop`

## Maliyet

- Suno Pro: $10/ay (tek yeni harcama, ay sonu iptal opsiyonel).
- ElevenLabs, Google AI Studio Max, Kling free, DaVinci free: $0 ek.
- Meta Ads test budget: ~EUR 350 (Fase 5, M karari).

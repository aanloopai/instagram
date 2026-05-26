# AanloopAI Instagram Reklam — Production Tasks

> **Konsept**: A — "De Reddingsbrigade" (5 super-kahraman, 25 sn Reels master)
> **Brief**: `C:\Users\Hallo\Desktop\aanloopai_instagram_reklam_brief_v2.md` v2.0
> **Plan**: `C:\Users\Hallo\.claude\plans\lexical-giggling-token.md` (onayli)
> **Olusturuldu**: 2026-05-26
> **Toplam ek maliyet**: $10/ay (Suno Pro)

---

## Fase 0 — Setup (~2 saat)

- [x] Repo skeleton olustu (`mkdir`, klasor yapisi). [DONE — automated]
- [x] `CLAUDE.md` yazildi. [DONE]
- [x] `README.md` yazildi. [DONE]
- [x] `.gitignore` yazildi. [DONE]
- [x] `.env.example` yazildi. [DONE]
- [x] `.env` lokal olustu (gitignored). [DONE 2026-05-26]
- [ ] Python venv: `python -m venv .venv` + activate.
- [ ] Deps: `pip install google-generativeai elevenlabs python-dotenv PyJWT requests`.
- [ ] `python scripts/verify_apis.py` calistir, output OK.
- [x] Brand logo `assets/logo/aanloopai.svg` kopyalandi (aanloop ana repo'dan). [DONE — 5 SVG/PNG]
- [ ] Brand logo PNG 200x60 transparent bug version hazirlandi (DaVinci veya Inkscape).
- [ ] ElevenLabs Voice Library tarama: `GET /v1/voices?language=nl` -> 6 voice ID sec, `.env`'e yaz.
- [ ] (Opsiyonel) ElevenLabs Voice Lab clone: kendi sample'in ile NL ses uret (Erbil veya fallback ses).
- [x] `git init` + ilk commit: `d4780ed`. [DONE]

---

## Fase 1 — Pre-production (~4 saat)

### Karakter portreleri (Imagen 4)

- [ ] `make characters` calistir -> 15 PNG (5 karakter x 3 angle: frontal, 3/4, profile).
- [ ] Output `assets/characters/` icinde dogrula (15 dosya var mi?).
- [ ] Her karakterin frontal'ina M-onay (visual QA, Rotterdam multicultural mix dogru mu?).
- [ ] Kling AI Face Reference Library'ye 5 karakter yukle (MANUEL — Kling web UI).
- [ ] Her face reference'a unique label ver: `destem-character`, `desecretaresse-character`, vb.

### Voiceover (ElevenLabs)

- [ ] `make vo` calistir -> 8 MP3 (`assets/audio/vo/shot##_character.mp3`).
- [ ] Her VO'yu dinle, telaffuz QA (NL dogru mu? "AanloopAI" net mi?).
- [ ] Sesleri saklamak gerekirse re-generate (stability 0.45 -> 0.55 dene).

### Jingle (Suno Pro — MANUEL, M ile birlikte)

> **Suno API durumu (2026-05-26)**: Suno resmi public API YOK — sadece enterprise/internal endpoint. 3rd-party reverse-engineered proxy'ler (sunoapi.org, suno-api GitHub) var ama TOS riskli ve unstable. **Karar: web UI manuel uretim, stem export Suno Pro panelinden.**

**Jingle tek-bakista spec** (brief section 6.1 + storyboard):

| Parametre | Deger |
|---|---|
| Hece | 3 (AAN - LOOP - AY) |
| Motif | Sol -> La -> Do (yukselen, cozulen) |
| Tonalité | D minor (warm, brand) |
| Tempo | 90 BPM |
| Ses | 7-kisilik karma-cinsiyet koro, 25-45 yas, warm Dutch accent |
| Enstruman | Sadece vokal + tek deep synth pad (Moog-style) son 800 ms swell |
| Drum | YOK |

**3 versiyon gerekli**:
1. **Intro** — 1.8 sn forte abrupt cut (shot 04-06 transition icin).
2. **Outro** — 2.0 sn sustained + synth swell tail (shot 12 final icin).
3. **Loop** — 4 sn extended loop (telefon hold music + diger re-use icin).

**M-action**:
- [x] Suno Pro web UI log-in. [DONE]
- [x] `prompts/suno/jingle.txt` -> Custom Mode prompt paste. [DONE]
- [x] Varyant uret + M sec. [DONE 2026-05-26 — https://suno.com/s/HS5kYHubXJE3Byda]
- [ ] **Suno'dan stem export**: vocal + synth pad ayri WAV (DaVinci re-mix icin).
- [ ] Suno'dan ana mix WAV indir -> `assets/audio/jingle/jingle_master.wav`.
- [ ] DaVinci'de 3 versiyon kes:
  - `assets/audio/jingle/intro.wav` (1.8 sn forte cut)
  - `assets/audio/jingle/outro.wav` (2.0 sn sustained + swell)
  - `assets/audio/jingle/loop_4s.wav` (4 sn loop, hold music re-use)

### Bed music (M yeni Suno run — `prompts/suno/bed_music.txt`)

> **Sebep (M kurali 2026-05-26)**: "Jingle altta hafif calmali, muzikle beraber. Konusmalar daha belirgin." 4-katmanli mix: VO foreground + jingle hits + bed music underscore + SFX. Detay: `tasks/audio_mix.md`.

- [ ] Suno Pro Custom Mode'a `prompts/suno/bed_music.txt` paste (Instrumental: ACIK — vokal-suz).
- [ ] D minor 90 BPM (jingle ile uyumlu), 25 sn cinematic underscore uret.
- [ ] 3 varyant, en iyiyi sec.
- [ ] Export: `assets/audio/bed/underscore_25s.wav`.

### Logo overlay assets

- [ ] `aanloopai.svg` -> 1920x1080 transparent PNG export (DaVinci shot 12 logo reveal).
- [ ] `aanloopai-bug.png` 200x60 transparent (shot 6'dan itibaren persistent).
- [ ] `aanloopai-signal.png` for shot 3 sky projection (oxblood gradient BG ile).

---

## Fase 2 — Production (~1 gun, Veo 3 generation tempo)

### Speaking shots (Veo 3 — Google AI Studio)

- [ ] `make video` calistir -> 6 MP4 generated.
- [ ] Shot 07 (De Stem telefon kapma) — lip-sync %95+ mi? Yoksa Sync.so pass.
- [ ] Shot 08 (De Secretaresse e-mail) — face reference Imagen ile tutarli mi?
- [ ] Shot 09a (De Stem van de Site chat balon) — split screen-ready format.
- [ ] Shot 09b (De Speurder LinkedIn lead) — split screen-ready format.
- [ ] Shot 10 (De Leermeester omuz dokunusu + Erbil yan plan) — duygu tonu sicak mi?
- [ ] Shot 12 (CTA + jingle resolve) — gercek logo overlay icin temiz BG.
- [ ] Tum 6 shot 9:16 1080x1920 24fps H.264 export.

### Action / b-roll shots (Kling AI API — `make kling`)

- [ ] `make kling` calistir -> 8 MP4 generated (`assets/video/kling/`).
- [ ] Shot 01 hook (Erbil eli + 23 missed call + yagmur).
- [ ] Shot 02 problem amplify (4 cut: WhatsApp + Gmail + saat + yuz).
- [ ] Shot 03 signal moment (Rotterdam skyline + Erasmusbrug + sky-projeksiyon).
- [ ] Shot 04 assemble silhouettes (5 lokasyon, 0.4 sn each).
- [ ] Shot 05 entry (ofis kapisi patlama, 5 silhouette giris).
- [ ] Shot 06 intro wide (5 kahraman tam cerceve + Erbil arkada).
- [ ] Shot 09 split BG (chat ofis + LinkedIn harita).
- [ ] Shot 11 resolution (Erbil gun isiginda gulumser, telefon 12 leads).
- [ ] Kling daily quota check (free tier kotaya yaklasinca shot bazli `--only` calistir).
- [ ] Tum 8 shot 9:16 H.264 dogrula.

### Audio prep

- [ ] Yagmur SFX (freesound.org CC-BY) -> `assets/audio/sfx/rain_loop.wav`.
- [ ] Kalp atisi bass-thump 60bpm -> `assets/audio/sfx/heartbeat_60bpm.wav`.
- [ ] Swoosh transition x 3 -> `assets/audio/sfx/swoosh_##.wav`.
- [ ] Synth swell sting (Moog-style, 1.2 sn) -> Suno'dan ekstra uret veya freesound.

---

## Fase 3 — Post (~1 gun, DaVinci Resolve)

### Timeline assemble

- [ ] DaVinci Resolve free yukle (eger yok ise).
- [ ] Yeni project 24fps 9:16 1080x1920 olustur.
- [ ] 14 video shot timeline'a yerlestir (6 Veo + 8 Kling).
- [ ] Shot suresi brief section 3.4 storyboard'a uy (0:00-0:25 = 25 sn).

### Audio mix (DETAYLI PROTOKOL: `tasks/audio_mix.md`)

4-katman: A1 VO (foreground -8dB) + A2 Jingle hits (intro+outro -6dB) + A3 Bed music underscore (-22dB sidechain) + A4 SFX (-18dB).

- [ ] A1 VO tracks 8 dosya hizalandi (shot 06/07/08/09a/09b/10/11/12).
- [ ] A1 EQ: HPF 200 Hz + presence +3 dB @ 3 kHz + de-ess.
- [ ] A1 Compressor: 3:1, threshold -18 dB.
- [ ] A2 Jingle intro yerlestir (shot 04-06 transition, otomasyon -6 dB hit).
- [ ] A2 Jingle outro yerlestir (shot 12 final, otomasyon -6 dB hit).
- [ ] A3 Bed music 25 sn underscore yerlestir (0-25s surekli -22 dB).
- [ ] A3 Sidechain compressor: VO key input, ratio 4:1, threshold -22 dB.
- [ ] A3 EQ: 1-4 kHz dip -4 dB (VO pocket).
- [ ] A4 Yagmur SFX shot 01-03 ambient.
- [ ] A4 Kalp atisi bass-thump shot 02 4 cut ile sync.
- [ ] A4 Synth swell shot 03 signal + shot 06 reveal.
- [ ] Master bus compressor 2:1 + normalize -14 LUFS + limiter -1 dBFS true peak.
- [ ] QA: headphone + telefon hoparlor + sound-off test.

### Overlay graphics

- [ ] Shot 03 sky-projection logo overlay (Erasmusbrug arkasi).
- [ ] Shot 06 bug logo persistent baslar (sol alt kose, kucuk).
- [ ] Shot 12 full logo reveal (tam ekran, oxblood gradient BG).
- [ ] Shot 07-10 lower-third caption animasyonlari (icon + NL text).
- [ ] Shot 01 hook caption sticker "23 gemiste oproepen. 1 ondernemer." (sol ust).
- [ ] Shot 11 caption "Welkom op je beste dag ooit."
- [ ] Shot 12 CTA text: `aanloopai.nl  •  Vanaf EUR 297/maand`.

### Color grade

- [ ] Oxblood + warm bone + Rotterdam-night-blue (#1a2540) paleti.
- [ ] ARRI Alexa LOG -> Rec.709 emulation LUT.
- [ ] Anamorphic lens flare effect shot 04, 05.
- [ ] Slight film grain pass.

### Final master

- [ ] Export H.264 25Mbps 9:16 1080x1920 24fps.
- [ ] Dosya: `assets/output/aanloopai_konsept_a_master_25s.mp4`.
- [ ] Caption-sound-off test (sound olmadan anlamli mi? Lower-thirds yeterli mi?).
- [ ] Hook 1.0 sn icinde 5-kisi blind test ("stop scroll" sinyali var mi?).

---

## Fase 4 — Variant cuts (~2 saat)

- [ ] **25 sn Reels master** (Konsept A primary) — DONE Fase 3 sonu.
- [ ] **9 sn Stories cut** — Konsept A'dan trim:
  - 0-1.5s hook (shot 01-02)
  - 1.5-5s reveal (shot 06 logo)
  - 5-8s 2 micro-action (shot 07 + shot 11)
  - 8-9s CTA (shot 12 last frame)
- [ ] **Konsept B "3:47 AM"** — DEFERRED (Wave-2, sadece Konsept A scale alirsa).
- [ ] **Konsept C "De Verdwijntruc" 6x6 sn** — DEFERRED (sadece A %20 alti dustugunde A/B icin reactive).

---

## Fase 5 — Launch

### Caption + creative

- [ ] 6 hook caption variant hazirla (brief section 10.1):
  1. "23 gemiste oproepen. 1 ondernemer. 5 redders."
  2. "Het is 23:47. Jij bent nog op kantoor. Lees verder."
  3. "Hollandse MKB'ers verliezen EUR 40.000 per jaar aan gemiste calls."
  4. "Ze noemen het AI. Wij noemen het: eindelijk slapen."
  5. "Wat als jouw bedrijf nooit meer offline was?"
  6. "Marvel had de Avengers. Jij hebt AanloopAI."
- [ ] Full caption template brief section 10.2 hashtag-set yaz.
- [ ] 4 CTA variant test (Boek demo / Bereken besparing / Zie in actie / Praat met Marco).

### Meta Ads

- [ ] Meta Ads Manager campaign olustur (CBO, broad NL targeting).
- [ ] Daily budget: EUR 50 ilk 7 gun = EUR 350 test.
- [ ] Conversion event setup (aanloopai.nl/?utm_source=meta).
- [ ] UTM tracking: `?utm_source=meta&utm_campaign=reddingsbrigade&utm_content={hook_id}`.
- [ ] Pixel + Conversions API setup (Brevo trackingleri uyumlu mu?).
- [ ] AanloopAI demo-inplannen landing icin custom conversion event.
- [ ] Campaign live: 6 hook x 1 ad each = 6 ad variant.

### Hook rate review (48 saat)

- [ ] 48 saat sonra ad-set-bazli hook rate (3-sec view rate) cek.
- [ ] %20 alti hook'lari kill.
- [ ] %30+ hook'lari scale (budget x 2, lookalike audience ekle).
- [ ] %20-30 arasi hook'lari iterate (caption rewrite + thumbnail variant).

### Post-launch monitoring

- [ ] 1 hafta sonra CPL + CAC hesapla.
- [ ] 2 hafta sonra ROI hesapla (3+ musteri = +60% ROI ay 1).
- [ ] Scale veya pivot karari M ile.
- [ ] `tasks/lessons.md` post-mortem update (Wave-2 oncesi).

---

## Statu

- **Aktif fase**: Fase 0 (Setup) — ~%70 tamamlandi.
  - Repo iskelet + commit `d4780ed` DONE.
  - `.env` lokal dolduruldu (4 API key: ElevenLabs + Google AI Studio + Kling + Pixabay) DONE.
  - Brand logo copy DONE.
- **Sonraki adim (M)**:
  1. `python -m venv .venv` + activate.
  2. `pip install google-generativeai elevenlabs python-dotenv PyJWT requests`.
  3. `python scripts/verify_apis.py` -> NL voice ID listele.
  4. `.env` icindeki 6 voice ID slotunu doldur.
- **Tahmini E2E**: 5-7 gun (Kling artik API'de, manuel UI gerek yok — daha hizli).
- **Jingle**: Suno Pro web UI manuel (API yok). Spec yukarida. M Fase 1 sirasinda paralel calisir.

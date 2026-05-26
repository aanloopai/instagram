# Audio Mix Protocol — DaVinci Resolve Fairlight

> **M kurali (2026-05-26)**: "Jingle altta hafif calmali, muzikle beraber. Konusmalar daha belirgin ve rahat anlasilir."

## Katmanli mimari (4 layer)

| Layer | Icerik | Hedef dB (RMS) | Notlar |
|---|---|---|---|
| **A1** | VO (ana konusmalar 8 shot) | **-8 dB ile -10 dB** | Foreground, EN belirgin |
| **A2** | Jingle hits (intro shot 04-06 + outro shot 12) | **-6 dB ile -8 dB** | Sadece hit anlarinda full, geri kalan SUS |
| **A3** | Background bed music (25 sn sinematik underscore) | **-22 dB ile -24 dB** | Surekli, VO altinda yumusak yorgan |
| **A4** | SFX (yagmur, kalp atisi, swoosh, synth swell) | **-18 dB ile -20 dB** | Spot bazli, shot 01-03 ambient |

## Suno'dan gelen 2 ayri kaynak

1. **Jingle** (M yapti — https://suno.com/s/HS5kYHubXJE3Byda):
   - Suno Pro'dan **stem export et**: vocal track + synth pad track ayri WAV.
   - 3 versiyon kes (DaVinci'de):
     - `intro.wav` — 1.8 sn forte cut (shot 04-06 transition).
     - `outro.wav` — 2.0 sn sustained + swell (shot 12 final).
     - `loop_4s.wav` — 4 sn (telefon hold music re-use, ana reklamda kullanilmaz).

2. **Bed music** (M yeni uretecek — `prompts/suno/bed_music.txt`):
   - 25 sn tek parca, cinematic underscore, D minor 90 BPM (jingle ile harmonic uyumlu).
   - Mid-freq pocket VO icin oyulmus (1-4 kHz dip).
   - Export: tek WAV `assets/audio/bed/underscore_25s.wav`.

## DaVinci Fairlight zincir (kanal bazli)

### A1 (VO tracks)
1. **EQ**: HPF 200 Hz (gurultu temizle), presence boost +3 dB @ 3 kHz, slight de-ess @ 6-8 kHz.
2. **Compressor**: 3:1 ratio, threshold -18 dB, attack 5 ms, release 80 ms, makeup +4 dB.
3. **Sidechain TRIGGER**: A1'in cikisi A3'un compressor key input'una gonderilir (ducking sebep).
4. **Output**: -8 dB averaj.

### A2 (Jingle hits)
1. **EQ**: HPF 80 Hz, boost +2 dB @ 200 Hz (warmth), slight roll-off > 12 kHz.
2. **Volume automation**:
   - 0-5s: -inf (sus).
   - 5-7s: -6 dB (intro hit shot 04-06).
   - 7-22s: -inf (sus, bed muzige birak).
   - 22-25s: -6 dB (outro shot 12 + final tonic swell).
3. **Output**: -6 dB hit anlarinda.

### A3 (Bed music)
1. **EQ**: 1-4 kHz dip -4 dB (VO pocket dynamic), boost +1 dB @ 80 Hz (warmth).
2. **Compressor SIDECHAIN**: Key input A1 (VO). Ratio 4:1, threshold -22 dB, attack 10 ms, release 200 ms.
   - **Etki**: VO geldigi an bed -4 dB ila -6 dB duser, VO bitince geri yukselir.
3. **Volume automation**:
   - 0-25s: surekli -22 dB (sidechain ile dinamik).
4. **Output**: -22 dB averaj.

### A4 (SFX)
- Per-shot spot, otomasyon ile shot 01-03 ambient yagmur (-20 dB), shot 02 4-cut heartbeat (-18 dB), shot 04-05 swoosh (-16 dB), shot 03+06 synth swell (-15 dB).

## Master bus

1. **Bus compressor**: SSL-style, 2:1 ratio, threshold -10 dB, slow attack 30 ms, fast release 100 ms, makeup +2 dB.
2. **Loudness normalize**: **-14 LUFS integrated** (Instagram standard), **-1 dBFS true peak limiter**.
3. **EQ master**: HPF 30 Hz (DC clean), slight presence shelf +0.5 dB @ 5 kHz.

## QA test seti

- [ ] Headphone test — VO her cumlede net anlasiliyor mu?
- [ ] Phone speaker test (Instagram audience) — bed muzik VO'yu boguyor mu?
- [ ] Spotify Loudness Meter ile -14 LUFS integrated dogrulama.
- [ ] True peak meter -1 dBFS asma kontrol.
- [ ] Sound-off test — caption + lower-third yeterli mi (sessiz izleyici icin)?

## Karar log

- **2026-05-26**: M Suno jingle yapti (https://suno.com/s/HS5kYHubXJE3Byda). Bed music yeni Suno run gerekli. Sidechain ducking ile VO belirginlik garantili.

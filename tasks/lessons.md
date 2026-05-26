# AanloopAI Reklam — Lessons (onceden uyari + post-mortem)

> Brief section 11.2 + production-time kesifler. Her sprint sonu update edilir.

## Onceden uyari (production baslamadan)

1. **AI estetigi saklanmali** — "hyper-real" hedefi, "stylized AI" degil. Imagen 4 + Veo 3 prompt'larda her zaman ARRI color science + cinematic + photorealistic + editorial fashion photography quality belirt.

2. **Speaking shot <= 4 saniye, <= 1 cumle**. Daha uzunu Veo 3 lip-sync'i kiriyor. Uzun monolog'lari pars et, multi-shot olarak yaz.

3. **Ses ONCE, video SONRA**. ElevenLabs WAV -> Veo 3 prompt'ina `[reference audio: shot07.wav]` parametresi ile bes. Asla ters sira.

4. **Logo ASLA AI ile uretilmez**. Her zaman vector overlay (DaVinci'de SVG/PNG layer). AI logo distortion = brand-killer.

5. **Hook rate 48 saat icinde stabilize olur**. %20 alti = kill, fix etme. %30+ = scale. %20-30 = caption rewrite + thumbnail variant.

6. **"AanloopAI" telaffuz reklam basina minimum 3 kez**. QA checklist'e sayilmali (target 4 — brief shot 6, 11, 12, 12-end).

7. **Cinsiyet-ses esleme zorunlu**:
   - Kadin karakter (De Secretaresse + De Speurder) -> kadin TTS.
   - Erkek karakter (De Stem + De Stem van de Site + De Leermeester) -> erkek TTS.
   - Anchor VO + Erbil -> erkek.

8. **Stories cut'lari Reels'ten direkt cut DEGIL**. Ayri kreatif olarak dusunulmeli (Konsept C path). Reels = hikaye, Stories = micro-hook + CTA snap.

9. **Veo 3 API method name'leri her sprint dogrulanmali**. Google API hizli evrildigi icin `dir(genai)` ile actual surface check zorunlu. `scripts/verify_apis.py` her run-once ile calisti.

10. **Kling Face Reference Library**'de karakter tutarliligi icin Imagen 4 frontal + 3/4 + profile uclemesi yuklenmeli. Sadece frontal yetersiz, profil olmazsa anamorphic angle'lar bozulur.

11. **Speaking shot'lari Veo 3'e, dialog-suz shot'lari Kling'e ver** — credit ekonomi. Brief section 8.5 split (6 Veo + 7-8 Kling) bu kurali yansitir. Tersine cevirme.

## Production-time kesifler (run sirasinda doldurulur)

_Empty — production basladiginda burasi update edilecek._

## Post-mortem (launch sonrasi)

_Empty — Fase 5 sonrasi 14 gun cikti analizinde update edilecek._

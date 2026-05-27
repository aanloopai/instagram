# Veo 3 image-to-video shot prompts — Konsept R

7 talking-head shot, hepsi 8s, hepsi narrator photo reference + lip-sync NL VO.

**Total talking-head sure**: 7 × 8s = 56s. Reklam toplam 1:14 (74s). Kalan ~18s
= grid-paper slide + floating UI screenshot insert frames + transitions.

## Shot mapping

| Shot | t | Beat | Ref portret | Expression |
|---|---|---|---|---|
| 01 | 0:00-0:08 | Hook + bridge | frontal.png | warm engaging direct |
| 02 | 0:09-0:16 | Brand reveal + product proof | three_quarter_left.png | slight turn conversational |
| 03 | 0:17-0:23 | Guarantee tease | frontal.png | eyebrows up emphasis |
| 04 | 0:24-0:34 | Mechanism + proof stat | three_quarter_right.png | slight gesture variety |
| 05 | 0:35-0:42 | Offer reveal + open loop | frontal.png | direct engaging question |
| 06 | 0:52-1:02 | Case study + result stat | three_quarter_left.png | storytelling |
| 07 | 1:03-1:14 | Social proof + CTA bridge | frontal.png | closing direct ask |

Pattern: frontal/3-4 alternate per Revido reference rhythm.

## Stat-verify gate (USER ACTION REQUIRED)

Shot 04 + Shot 06 contain placeholder rakam:
- Shot 04: "18 uur per week" + "4.200 euro per maand"
- Shot 06: "312 leads" + "14 procent" + "in 4 weken"

Spec mock-data ASLA kurali. User gercek anonim Aanloop rakam vermeden Veo 3
generate ETME. Eger gercek rakam farkliysa shot_04.txt + shot_06.txt VO satirini
edit et, sonra `make video-r` calistir.

## Brand reuse check

Shot 02 "AanloopAI" telaffuzu — Veo 3 omni TTS olarak NL natif, "Aan-loop-ay"
soylenir mi? Test sample sonrasi karar:
- Telaffuz OK → devam
- Telaffuz fail → ElevenLabs NL voice + DaVinci mux (Veo 3 sessiz video)

## Generation tempo

Veo 3 omni queue: ~3-8 dk/shot Google AI Studio. 7 shot = ~30-60 dk total.
Yan tarafta grid slide + UI screenshot composite paralel calisilabilir.

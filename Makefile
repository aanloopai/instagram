.PHONY: all verify characters narrator narrator-full vo video kling jingle assemble clean

all: verify characters vo video kling assemble

verify:
	@echo "==> API surface verification"
	python scripts/verify_apis.py

characters:
	@echo "==> Imagen 4: 5 character x 3 angle = 15 portraits (Konsept A)"
	python scripts/generate_characters.py

narrator:
	@echo "==> Imagen 4: NL-male IT-expert narrator (Konsept R) sample mode 2/angle"
	python scripts/generate_narrator.py

narrator-full:
	@echo "==> Imagen 4: NL-male IT-expert narrator (Konsept R) FULL 8/angle = 40 portraits"
	python scripts/generate_narrator.py --full

vo:
	@echo "==> ElevenLabs: 8 NL voiceovers"
	python scripts/generate_vo.py

video:
	@echo "==> Veo 3: 6 speaking shots (Google AI Studio)"
	python scripts/generate_veo3.py

kling:
	@echo "==> Kling AI API: 8 action / b-roll shots"
	python scripts/generate_kling.py

jingle:
	@echo "MANUEL: Suno Pro web UI"
	@echo "        Prompt: prompts/suno/jingle.txt"
	@echo "        Output: assets/audio/jingle/{intro,outro,loop_4s}.wav"

assemble:
	@echo "==> DaVinci Resolve FCP XML manifest"
	python scripts/build_davinci_project.py
	@echo ""
	@echo "MANUEL: DaVinci Resolve > File > Import > Timeline > assets/timeline.fcpxml"

clean:
	@echo "==> Removing AI-generated assets (regenerable)"
	@rm -rf assets/characters/*.png
	@rm -rf assets/audio/vo/*.mp3
	@rm -rf assets/video/veo3/*.mp4
	@rm -rf assets/video/kling/*.mp4
	@echo "    Done. Run 'make all' to regenerate."

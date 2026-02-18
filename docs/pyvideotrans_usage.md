# pyvideotrans -- Usage Documentation

## Overview
Video translation, speech transcription, AI dubbing, and subtitle translation tool. Supports multiple ASR engines (Whisper, FunASR), TTS providers (Edge-TTS, Elevenlabs), and translation APIs. CLI mode for headless Docker operation.

## Quick Start

```bash
docker pull hoomzoom/pyvideotrans
```

### Speech-to-Text
```bash
docker run --rm -v ./input:/input -v ./output:/app/output \
  hoomzoom/pyvideotrans --task stt --name /input/video.mp4
```

### Video Translation
```bash
docker run --rm -v ./input:/input -v ./output:/app/output \
  hoomzoom/pyvideotrans --task vtv --name /input/video.mp4 \
  --source_language_code zh --target_language_code en
```

## CLI Tasks

| Task | Description | Example |
|------|-------------|---------|
| stt | Speech-to-Text (audio/video to SRT) | `--task stt --name /input/audio.wav` |
| tts | Text-to-Speech (SRT to audio) | `--task tts --name /input/subs.srt --voice_role en-US-AriaNeural` |
| sts | Subtitle Translation | `--task sts --name /input/subs.srt --target_language_code en` |
| vtv | Full Video Translation | `--task vtv --name /input/video.mp4 --source_language_code zh --target_language_code en` |

## Key CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| --task | Required | Task type: stt, tts, sts, vtv |
| --name | Required | Input file path |
| --recogn_type | 0 | ASR engine: 0=faster-whisper, 1=openai-whisper |
| --model_name | base | Whisper model: tiny, small, base, medium, large-v3 |
| --source_language_code | None | Source language (zh, en, ja, etc.) |
| --target_language_code | None | Target language |
| --tts_type | 0 | TTS provider |
| --voice_role | None | Voice name for TTS |
| --cuda | False | Enable GPU acceleration |

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | No | None | For OpenAI Whisper/ChatGPT TTS |
| HF_HOME | No | /app/models | HuggingFace model cache |

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | CLI --help | PASS |
| 2 | FFmpeg available | PASS |
| 3 | Module imports | PASS |
| 4 | STT task (faster-whisper, tiny model) | NOT TESTED (requires model download) |

## Notes
- First run downloads ASR/TTS models (can be GB-scale for large models).
- Mount `/app/models` as volume to persist downloaded models across runs.
- Mount `/app/output` to retrieve results.
- CPU-only by default. For GPU, use NVIDIA runtime and `--cuda` flag.
- Python 3.10 strictly required.

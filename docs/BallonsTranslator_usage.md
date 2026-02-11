# BallonsTranslator. Usage Documentation

## Overview
Headless manga and comic image translator. Runs OCR detection, text inpainting, and machine translation in batch mode. No GUI is exposed. All processing is driven through the CLI entry point. Supports DeepL, OpenAI, and several free translation backends.

## Quick Start
```bash
docker pull hoomzoom/ballonstranslator
docker run --rm \
  -v /path/to/manga:/input \
  -v /path/to/output:/output \
  hoomzoom/ballonstranslator \
  --exec_dirs /input
```

Translated images are written to the directory alongside their originals by default. Mount a separate `/output` path and pass it to the relevant config option if you want output isolated.

## Entry Point
```
python launch.py --headless [OPTIONS]
```

The container ENTRYPOINT is `python launch.py --headless`. Arguments appended to `docker run` are passed through directly.

### Common Arguments
| Argument | Description |
|---|---|
| `--exec_dirs /input` | Directory of source images to translate |
| `--config_path /app/config.json` | Path to a BallonsTranslator config file |

## Volume Mounts
| Mount | Purpose |
|---|---|
| `/input` | Source manga or comic images (bind mount from host) |
| `/output` | Translated output images (optional, bind mount from host) |

## Environment Variables
| Variable | Required | Default | Description |
|---|---|---|---|
| QT_QPA_PLATFORM | Set in image | offscreen | Forces PyQt6 into headless mode. Do not override. |
| DEEPL_AUTH_KEY | No | None | DeepL API key for DeepL translation backend |
| OPENAI_API_KEY | No | None | OpenAI API key for GPT translation backend |

API keys are optional at container startup. They are only required if the selected translation backend needs them. Free backends (e.g., Google Translate via the translators library) work without any key.

## Health Check
The container health check runs:
```
python -c "import torch; import cv2"
```
This confirms PyTorch (CPU) and OpenCV loaded correctly. There is no HTTP endpoint.

## QC Test
```bash
docker run --rm hoomzoom/ballonstranslator python -c "import torch; import cv2; print('ok')"
```
Expected output: `ok`

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- PyTorch is CPU-only. GPU is not used even if a CUDA-capable GPU is present.
- PyQt6 is installed and loaded in offscreen mode (QT_QPA_PLATFORM=offscreen). No display is needed.
- MeCab and its UTF-8 dictionary are installed for Japanese morphological analysis.
- The `pillow-jxl-plugin` and Windows-specific packages from the upstream requirements are excluded as they are not compatible with the Linux slim base.
- No port is exposed. This is a pure batch processing tool.

## Changes from Original
- No upstream Dockerfile existed. Dockerfile written from scratch.
- CPU-only PyTorch installed first via the PyTorch CPU wheel index to prevent CUDA builds from being pulled in transitively.
- `pillow-jxl-plugin` excluded (requires non-standard Pillow build flags).
- Windows-specific packages excluded.
- Non-root user added.
- HEALTHCHECK uses `import torch; import cv2` since there is no HTTP endpoint.

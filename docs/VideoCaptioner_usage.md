# VideoCaptioner -- Local Install Guide

## Overview
VideoCaptioner is a desktop application for automated video subtitle generation. It uses speech recognition and optionally LLMs to transcribe audio, generate subtitles, and burn them into video files. The interface is a PyQt5 desktop GUI.

## Why Not Dockerized
VideoCaptioner requires a graphical display. The PyQt5 interface cannot run in a headless Docker container without a virtual display server, and the application has no headless or CLI mode. It is designed to be operated interactively by a user on a desktop.

## Requirements
- OS: Windows 10/11 (primary target). Linux with a desktop environment should also work.
- Python 3.9 or newer
- pip
- FFmpeg installed and on PATH
- A display (physical or virtual)

## Installation

**From PyPI:**

```bash
pip install videocaptioner
```

**From source:**

```bash
git clone https://github.com/WEIFENG2333/VideoCaptioner.git
cd VideoCaptioner
pip install -r requirements.txt
```

Install FFmpeg if not already available:
- Windows: download from https://ffmpeg.org/download.html and add to PATH, or use `winget install ffmpeg`.
- Linux: `sudo apt install ffmpeg`

## Usage

**If installed via pip:**

```bash
videocaptioner
```

**If running from source:**

```bash
python main.py
```

The desktop GUI will open. Load a video file, configure the subtitle language and output settings, then run the captioning pipeline. Subtitles can be exported as SRT files or burned directly into the video.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OpenAI API key | Optional (via UI) | None | Required only if using LLM-assisted subtitle refinement |

## Notes
- The core speech-to-text pipeline works without an API key using local models. LLM-assisted polishing requires an OpenAI key configured in the app settings.
- On Linux, ensure a desktop environment is running before launching. A virtual display via Xvfb will not provide the full interactive experience.
- GitHub: https://github.com/WEIFENG2333/VideoCaptioner

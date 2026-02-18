# Windrecorder -- Local Install Guide

## Overview
Windrecorder is a Windows-only personal memory search app that continuously records your screen, indexes content via OCR, and lets you search or rewind through past screen activity. It runs entirely locally with no cloud uploads.

## Why Not Dockerized
Windrecorder uses Windows-only system APIs (pywin32, Windows OCR via wcocr, ffmpeg integration) to capture the screen and record desktop activity. Docker containers on Windows do not have access to the host desktop or display. The tool also uses `.bat` scripts for installation and startup, and is explicitly designed as a Windows desktop utility.

## Requirements
- OS: Windows 10 or 11 (required; no Linux or macOS support)
- Python 3.11 (specifically; 3.12 is not currently supported)
- Git
- FFmpeg (must be in `C:\Windows\System32\` or in PATH)
- 10-20 GB free disk space per month of recordings
- No GPU required (uses CPU-based OCR)

## Installation

### Step 1: Install prerequisites

Install Git from https://git-scm.com/downloads.

Install Python 3.11 from https://www.python.org/downloads/ -- check "Add Python to PATH" during installation.

Install FFmpeg:
```
Download from https://ffmpeg.org/download.html
Extract and copy ffmpeg.exe, ffprobe.exe to C:\Windows\System32\
```

### Step 2: Clone and install

```bash
git clone https://github.com/yuka-friends/Windrecorder.git
cd Windrecorder
```

Double-click `install_update.bat` (or run it from a terminal):

```cmd
install_update.bat
```

This creates a virtual environment, installs Python dependencies, and configures the app.

### Step 3: Launch

Double-click `start_app.bat` (or run from terminal):

```cmd
start_app.bat
```

This opens the Windrecorder Streamlit web UI in your default browser (typically at `http://localhost:8501`).

## Usage

1. Launch via `start_app.bat`.
2. In the UI, go to **Settings** to configure recording interval, storage path, and OCR engine.
3. Click **Start Recording** to begin continuous screen capture. Windrecorder takes a screenshot every 3 seconds (default), compresses sequences into video every 15 minutes.
4. Use the **Search** tab to query past screen content by text (OCR) or image description.
5. Use the **Rewind** tab to browse recorded video by time.

## Notes
- OCR engines available: Rapid OCR (built-in, cross-language), WeChat OCR (Windows only, better Chinese support), Tesseract (must install separately).
- Storage estimate: approximately 10-20 GB per month at default settings.
- Recording can be paused from the system tray icon.
- The repo is maintained under yuka-friends/Windrecorder (not Antonoko/Windrecorder as originally attributed).
- GitHub: https://github.com/yuka-friends/Windrecorder

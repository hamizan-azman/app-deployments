# AiNiee -- Local Install Guide

## Overview
AiNiee is a desktop AI translation tool with a PyQt5/PyQt-Fluent-Widgets GUI that automates bulk translation of games, novels, subtitles, and documents using AI APIs (OpenAI, DeepL, local models via Ollama/LM Studio, and others).

## Why Not Dockerized
AiNiee is a PyQt5 desktop GUI application with no headless or CLI mode. It requires a display server to render its interface and accepts input through its GUI (drag-and-drop file loading, button clicks, settings dialogs). There is no way to run it meaningfully without a desktop session.

## Requirements
- OS: Windows 10/11 (primary and best-supported); Linux with a desktop environment may work
- Python 3.11 or 3.12
- No GPU required for cloud API translation; GPU optional for local model backends
- An API key for at least one translation backend (OpenAI, DeepSeek, etc.) or a local model server (Ollama, LM Studio)

## Installation

### Option 1: Prebuilt release (recommended for Windows)

Download the latest `.exe` installer or portable `.zip` from the releases page:

```
https://github.com/NEKOparapa/AiNiee/releases
```

Extract and run `AiNiee.exe`. No Python installation required.

### Option 2: Run from source

```bash
# Clone the repo
git clone https://github.com/NEKOparapa/AiNiee.git
cd AiNiee

# Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux

# Install dependencies
pip install -r requirements.txt

# Launch the application
python main.py
```

## Usage

1. Open the application (installer or `python main.py`).
2. Go to **Settings** and enter your API key and select a translation engine.
3. Drag a folder containing source files (game scripts, `.epub`, `.srt`, `.txt`, `.docx`, etc.) into the application window, or use the file picker.
4. Configure source and target languages.
5. Click **Start** to begin translation.
6. Translated files are written to the output directory specified in Settings.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (none) | -- | -- | All configuration (API keys, model selection, paths) is done through the GUI settings panel |

## Notes
- AiNiee supports many translation providers: OpenAI, Anthropic, DeepSeek, Gemini, DeepL, Cohere, local Ollama, LM Studio, and others.
- The tool is primarily designed for game text formats exported by tools like Mtool, Translator++, and Renpy.
- GitHub: https://github.com/NEKOparapa/AiNiee

# AI_NovelGenerator. Local Install Guide

**Deployment**: Workstation. Cross-platform desktop GUI on Linux/Win/macOS.

## Overview
AI_NovelGenerator is a desktop tool for long-form Chinese or English novel writing with LLM assistance. It maintains an outline, chapter skeletons, character cards, and a vector memory of prior chapters, then prompts an LLM to expand each chapter while staying consistent with the stored context.

## Why Not Dockerized
The application is a CustomTkinter desktop GUI.

- `main.py` constructs a `customtkinter.CTk()` root window and runs `root.mainloop()`.
- All user interaction (novel setup, chapter-by-chapter generation, edits, exports) happens through Tkinter widgets. There is no CLI mode and no HTTP server.
- `customtkinter` is a wrapper over Tkinter, which requires a display server.

Docker containers without an X server have no way to render the window, and the project ships no headless generator script. The app is therefore skipped.

## Requirements
- OS. Windows 10/11 (primary), macOS 12+, or Linux with a desktop environment
- Python 3.10 or 3.11
- `pip`
- An OpenAI-compatible LLM endpoint (OpenAI, DeepSeek, a local Ollama or LM Studio server)
- An embeddings endpoint (OpenAI embeddings or a local embedding model)

## Installation

```bash
git clone https://github.com/YILING0013/AI_NovelGenerator.git
cd AI_NovelGenerator

python -m venv venv
venv\Scripts\activate             # Windows
# source venv/bin/activate        # Linux/macOS

pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The main window opens with four tabs.

1. Main Settings. LLM base URL, API key, model, embeddings model, temperature, max tokens.
2. Novel Settings. Title, theme, genre, target length, character cards, outline.
3. Writing. Chapter-by-chapter generation with a text editor for review.
4. Logs. Prompt and response history for debugging.

Fill in the LLM and embeddings endpoints first, then author the novel settings, then iterate on chapters from the Writing tab.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (none)   | . | . | All configuration lives in the GUI. Persisted to `config.json` next to `main.py` |

## Notes
- The OpenAI base URL field accepts any OpenAI-compatible endpoint (DeepSeek, Ollama, LM Studio). Use `http://localhost:11434/v1` for a local Ollama install.
- Vector memory is stored in `./novel_memory`. Delete the folder to reset.
- Verified: source install `pip install -r requirements.txt` succeeds in a Python 3.11 venv on Ubuntu WSL, 27 April 2026. GUI launch was not exercised. That requires WSLg or a Windows / Linux desktop session.
- GitHub. https://github.com/YILING0013/AI_NovelGenerator

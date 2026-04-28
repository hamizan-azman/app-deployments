# Open-Interface. Local Install Guide

**Deployment**: Workstation with display + accessibility permissions (macOS-primary, also Linux/Windows).

## Overview
Open-Interface is an LLM-driven desktop assistant that takes natural-language instructions and executes them on the host by moving the mouse, typing, and reading the screen. It is a Python `tkinter` application that runs in the system tray.

## Why Not Dockerized
Open-Interface controls the host's physical input devices and reads the host display. Concretely.

- It uses `pyautogui` for mouse and keyboard synthesis, which requires a connected display server.
- It takes screenshots with `mss` and `Pillow.ImageGrab`, which have no meaning inside a container without an X, Quartz, or DirectX surface.
- The UI itself is `tkinter`, which needs a display.
- Several dependencies in `requirements.txt` are macOS-only (`pyobjc-framework-Cocoa`, `pyobjc-framework-Quartz`), and the mainline install path targets macOS first.

A container with no display and no input device cannot run any of this in a useful way.

## Requirements
- OS. macOS 12+ (primary target), Windows 10/11, or Linux with a full desktop environment
- Python 3.11
- A visible desktop session (not a headless SSH session)
- OpenAI API key with access to a multimodal model (gpt-4o recommended)
- Accessibility permissions granted. On macOS. System Settings, Privacy & Security, Accessibility and Screen Recording

## Installation

```bash
git clone https://github.com/AmberSahdev/Open-Interface.git
cd Open-Interface

python3.11 -m venv venv
source venv/bin/activate             # Linux/macOS
# venv\Scripts\activate              # Windows

pip install -r requirements.txt
```

On macOS, approve Accessibility and Screen Recording for the Terminal or IDE that will launch the app.

## Usage

```bash
source venv/bin/activate
python app/app.py
```

A small window appears with an input box. Type the task in English ("open Safari and search for Claude") and press Enter. The agent takes control of the cursor and keyboard until it declares the task complete. Press the stop hotkey (default `Cmd+Shift+Q`) to abort.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | Entered through the GUI Settings panel. Cached in `settings.json` |

## Notes
- macOS Accessibility permission is the most common setup failure. If the cursor does not move, re-check the permissions list.
- For reproducibility in research, run on a fixed screen resolution and a pinned OS theme. The vision model's click coordinates are resolution-sensitive.
- GitHub. https://github.com/AmberSahdev/Open-Interface

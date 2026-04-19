# Cradle. Local Install Guide

## Overview
Cradle is BAAI's general-purpose computer-control agent. The public release drives real desktop games (Red Dead Redemption 2, Cities. Skylines, Stardew Valley) and productivity apps (Chrome, Office) by observing the screen with a multimodal LLM and producing mouse, keyboard, and controller actions. Mobile support is provided through ADB.

## Why Not Dockerized
Cradle expects to run on a full Windows desktop next to the target application.

- Input is synthesised through `pyautogui`, `pydirectinput`, and low-level Windows calls (`SendInput`).
- Screen capture uses DirectX, MSS, and Windows `BitBlt`. None of these work in a container.
- Game targets (RDR2, Skylines) require the game to be launched on the host and visible.
- The mobile runner uses ADB against a physically-connected or emulated Android device. `adb` needs USB or emulator port forwarding that is not part of a clean Docker environment.
- The repo ships no Dockerfile.

Even ignoring the games, the agent framework assumes real keyboard and mouse events, which Docker containers cannot generate.

## Requirements
- OS. Windows 10/11 (primary). Linux partial support. macOS not officially supported
- Python 3.10 via Conda or Miniconda
- NVIDIA GPU strongly recommended (the vision reasoning loop is heavy)
- A multimodal LLM. GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 (configured in `conf/`)
- For mobile runs. ADB plus a connected Android device or emulator
- For game runs. The target game installed and runnable on the host

## Installation

```powershell
git clone https://github.com/BAAI-Agents/Cradle.git
cd Cradle

conda create -n cradle python=3.10 -y
conda activate cradle

pip install -r requirements.txt
```

Edit `conf/env_config_<env>.json` for your LLM keys and pick the target environment (`rdr2`, `skylines`, `stardew`, `chrome`, `outlook`).

## Usage

Launch the target application (start RDR2 and load a save). Then, in the conda env.

```powershell
conda activate cradle
python runner.py --envConfig conf\env_config_rdr2.json
```

The agent begins screenshotting, reasoning, and sending input events. Keep the game or app window focused and unminimised.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY    | Conditional (GPT backend)   | None | Loaded by the environment config |
| ANTHROPIC_API_KEY | Conditional (Claude backend)| None | Same |
| GEMINI_API_KEY    | Conditional (Gemini backend)| None | Same |

## Notes
- For reproducibility in research, pin the game or app version. Even minor updates shift UI coordinates.
- The repo contains several "skill library" JSON files per target. Leave these intact. Deleting them degrades the agent.
- GitHub. https://github.com/BAAI-Agents/Cradle

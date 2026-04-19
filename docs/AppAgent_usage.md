# AppAgent. Local Install Guide

## Overview
AppAgent is Tencent's LLM-driven mobile-app agent. It connects to an Android device via ADB, captures the current UI as an XML hierarchy plus screenshot, feeds both into a multimodal LLM, and emits `tap`, `long_press`, `swipe`, `type`, and `back` actions to complete user tasks inside arbitrary Android apps.

## Why Not Dockerized
AppAgent needs a physical or emulated Android device reachable by ADB.

- `adb shell uiautomator dump` extracts the current UI tree.
- `adb exec-out screencap` captures the screenshots the vision model sees.
- `adb shell input tap / swipe / text / keyevent` is how every action reaches the phone.
- The repo has no standalone or desktop mode. Removing the device removes the only input and output surface.

Running ADB inside a container is technically possible (it is a user-space binary), but the connection to the phone requires USB passthrough (unavailable on Docker Desktop or WSL2 without extra third-party drivers), or a network-reachable emulator with the emulator's adb-server port bridged. Neither is a clean, one-command container deployment. Neither gives a self-contained reproducible unit the benchmark can grade. The upstream project runs on a host with ADB and a connected device or emulator.

## Requirements
- OS. Windows 10/11, macOS, or Linux
- Python 3.9 or newer
- Android SDK platform-tools (`adb`) on PATH
- An Android device (physical or emulator) with USB debugging enabled
- Android 11+ recommended for reliable UIAutomator dumps
- OpenAI API key with a multimodal model (gpt-4-vision, gpt-4o)

## Installation

```bash
git clone https://github.com/TencentQQGYLab/AppAgent.git
cd AppAgent

python -m venv venv
source venv/bin/activate           # Linux/macOS
# venv\Scripts\activate            # Windows

pip install -r requirements.txt
```

Verify `adb` sees the device.

```bash
adb devices        # should list your device as "device" (not "unauthorized")
```

Edit `config.yaml` with your LLM model name and API key.

## Usage

Two modes ship with the project.

Exploration mode (agent learns an app's UI first).

```bash
python learn.py
```

Enter the app package name or pick from the list. The agent opens the app and explores it autonomously, saving a `docs/<app>.json` knowledge file.

Task mode (agent completes a user-stated task).

```bash
python run.py
```

Enter the app and the natural-language instruction ("open the second conversation in WeChat and reply with hello"). The agent chooses actions and submits them to the device.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | Read from `config.yaml` via the `api_key` field |

## Notes
- Default Android emulator images for development. Pixel 6, API 33, factory AOSP build. Running against Xiaomi or OPPO OEM builds sometimes breaks UIAutomator dumps.
- The agent is conservative. By default it waits 3 seconds between actions. Reduce this in `config.yaml` only if the target app's animations are fast enough.
- GitHub. https://github.com/TencentQQGYLab/AppAgent

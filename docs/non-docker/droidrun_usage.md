# droidrun -- Local Install Guide

**Deployment**: Workstation + connected Android (or iOS) device via ADB.

Known upstream issue (verified 27 April 2026). `pip install droidrun` (currently 0.5.9) installs cleanly, but `from droidrun import DroidAgent` fails with `ImportError: cannot import name 'AsyncMobilerun' from 'mobilerun'`. The reason is that droidrun's `tools/driver/cloud.py` imports a class that the latest `mobilerun` package (0.6.0rc2) no longer exports. The two packages are mid-migration. The upstream renamed the GitHub repo from `droidrun/droidrun` to `droidrun/mobilerun`, and the Python package surface is being split between them. Track the upstream issue tracker for a coordinated `droidrun + mobilerun` version pair before relying on this in production. As a workaround, pin to the last known-working pair once one is established.

## Overview
droidrun is a framework for AI-driven Android and iOS device control. It connects to a physical device via ADB (Android Debug Bridge) and allows LLM agents to interact with the device by issuing taps, swipes, text inputs, and app launches. It is designed for building automated mobile testing and agent workflows.

## Why Not Dockerized
droidrun requires a physical Android or iOS device (or emulator) connected to the host machine via ADB over USB or TCP. Docker containers cannot access USB devices or ADB sockets without complex host-side passthrough configuration, and even then the tool is fundamentally designed to run on the host system alongside the connected device. There is no meaningful way to containerise the device-control layer.

## Requirements
- OS: macOS, Linux, or Windows
- Python 3.10 or newer
- pip
- ADB installed and on PATH (Android Debug Bridge, part of Android SDK Platform Tools)
- An Android device with USB debugging enabled, connected via USB or ADB-over-WiFi. iOS support requires additional setup per the README.
- OpenAI API key or compatible LLM provider

## Installation

```bash
pip install droidrun
```

To install from source:

```bash
git clone https://github.com/droidrun/mobilerun.git
cd droidrun
pip install -e .
```

Install ADB if not already available:
- macOS: `brew install android-platform-tools`
- Ubuntu/Debian: `sudo apt install adb`
- Windows: download Android SDK Platform Tools from https://developer.android.com/tools/releases/platform-tools and add to PATH

## Device Setup

Enable USB debugging on the Android device:
1. Go to Settings, then About Phone, and tap Build Number seven times to enable Developer Options.
2. Go to Settings, then Developer Options, and enable USB Debugging.
3. Connect the device via USB and accept the RSA key prompt on the device.

Verify the connection:

```bash
adb devices
```

The device should appear as `<serial> device`. If it shows `unauthorized`, accept the prompt on the phone screen.

## Usage

droidrun is used as a Python library or via its CLI. A minimal agent example:

```python
import asyncio
from droidrun import DroidAgent

async def main():
    agent = DroidAgent(
        goal="Open the calculator app and compute 42 plus 58",
        llm_provider="openai",
        model="gpt-4o"
    )
    await agent.run()

asyncio.run(main())
```

Or via the CLI (check `droidrun --help` for current flags):

```bash
droidrun run --goal "Open Chrome and navigate to example.com" --model gpt-4o
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes (for OpenAI backend) | None | API key for the LLM that drives the agent |
| `ANDROID_SERIAL` | Optional | First ADB device | ADB serial number of the target device if multiple are connected |

## Notes
- ADB emulators (Android Studio AVD, Genymotion) can substitute for a physical device on the same host machine. Start the emulator before running droidrun and it will appear in `adb devices`.
- iOS support requires additional tooling. See the droidrun README for iOS-specific setup steps.
- droidrun takes screenshots of the device screen to give the LLM visual context. Ensure the device screen is on and unlocked during agent runs.
- GitHub: https://github.com/droidrun/mobilerun (the upstream renamed the repo from `droidrun` to `mobilerun` in early 2026. The PyPI package is still `pip install droidrun`.)

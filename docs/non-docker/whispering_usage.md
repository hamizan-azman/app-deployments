# whispering. Local Install Guide

**Deployment**: Workstation with microphone (Tauri desktop app).

## Overview
Whispering (braden-w/whispering) is a desktop speech-to-text app built with Tauri and Svelte: press a global shortcut, speak, and get transcribed text. It uses OpenAI's Whisper API or a local Whisper backend.

## Why Not Dockerized
Whispering is a native desktop application that requires access to the host microphone and system audio subsystem. Docker containers cannot access audio input devices without complex OS-level passthrough that is not supported on Windows. The app also has a system-tray GUI component that requires a display.

## Requirements
- OS: Windows, macOS, or Linux (desktop required)
- Microphone or audio input device
- Node.js 18+ and pnpm (for building from source)
- Rust toolchain (for building from source via Tauri)
- OpenAI API key (for cloud Whisper) or local Whisper setup

## Installation

### Option 1: Download prebuilt installer (recommended)

Download the latest release for your OS from the releases page:

```
https://github.com/braden-w/whispering/releases
```

Run the installer (`.msi` on Windows, `.dmg` on macOS, `.AppImage` or `.deb` on Linux).

Note: the project has migrated to the EpicenterHQ organization. The current release page is:

```
https://github.com/EpicenterHQ/epicenter/releases
```

### Option 2: Build from source

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Node.js 18+ and pnpm
npm install -g pnpm

# Clone the repo
git clone https://github.com/braden-w/whispering.git
cd whispering

# Install JS dependencies
pnpm install

# Build and run the Tauri desktop app
pnpm tauri dev
```

## Usage

1. Launch the app from the installer or with `pnpm tauri dev`.
2. Enter your OpenAI API key in Settings (for cloud transcription).
3. Press the configured global shortcut (default: `Ctrl+Shift+.` on Windows).
4. Speak. Release the shortcut or press Stop.
5. Transcribed text is copied to clipboard and/or inserted at cursor.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes (via UI) | None | Entered in the app settings. used for Whisper API calls |

## Notes
- The original braden-w/whispering repository has been archived and redirects to EpicenterHQ/epicenter. Check that repo for the latest release.
- Local Whisper (no API key) requires a separate Whisper server. see the app settings for supported local backends.
- Verified end-to-end on Windows host, 27 April 2026. Prebuilt `.msi` installer downloaded from EpicenterHQ/epicenter releases, installed cleanly. Live mic capture plus transcription via the OpenAI Whisper API confirmed working.
- GitHub: https://github.com/braden-w/whispering (archived, redirects to https://github.com/EpicenterHQ/epicenter)

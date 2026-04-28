# autoMate. Local Install Guide

**Deployment**: Workstation with desktop and browser control. The full feature set is RPA (pyautogui, playwright). The server-and-storage core can run headless if only the MCP / SaaS bridge is needed.

## Overview

autoMate is a "smart NAS for AI", a personal data hub plus tool source that exposes notes, files, reminders, memory, audio transcription, and 30+ SaaS connectors to AI clients (OpenClaw, Claude Desktop, Cursor, Cline, Kimi) over MCP-over-HTTP. It can also be used standalone through its built-in web chat. Data lives in a SQLite database under `~/.automate/` with Fernet-encrypted secrets.

Upstream replaced the project we had documented with a different one. The v0.x we wrote about was an OmniParser-based desktop RPA tool with a Gradio UI at port 7888 and a `python install.py` step that pulled around 2 GB of OmniParser weights. v4.5.7 (the current version) is the MCP-over-HTTP hub described above. Same maintainer (`yuruotong1/autoMate`), same repo URL, completely different product. The OmniParser pipeline, the Gradio UI, and the `install.py` script are gone.

## Why classified as workstation

The full agent (`pip install 'automate-hub[full]'`) pulls in pyautogui (desktop control), playwright (browser automation), and pywin32 (Windows-specific). These need a live desktop session and host display. A headless server cannot produce the inputs autoMate's desktop tools generate.

The minimal core (`pip install automate-hub` without extras) is just the FastAPI server, storage layer, and MCP endpoint. That part runs cleanly in Docker. Upstream provides a Dockerfile and a published image at `ghcr.io/yuruotong1/automate:latest` for that headless mode. Our classification stays "workstation" because the full agent path is what most users run day-to-day.

## Requirements

- OS: Windows 10/11, macOS, or Linux desktop
- Python 3.10 or newer
- A multimodal LLM provider key (OpenAI, Anthropic, Gemini, Mistral, DeepSeek, Moonshot, GLM, and 19 more in the catalog)
- Optional, only for the full extras:
  - Chromium for playwright (`python -m playwright install chromium`, around 150 MB)
  - A real desktop session. The `[full]` install cannot run on a headless server.
- Around 150 MB free disk space for the install plus whatever your `~/.automate/` data grows to over time

## Installation

### Path 1: PyPI (recommended)

```bash
pip install 'automate-hub[full]'
```

### Path 2: From source

```bash
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate
pip install '.[full]'
```

### Path 3: Standalone binary

Pre-built Windows, macOS, and Linux binaries are published at https://github.com/yuruotong1/autoMate/releases/latest. Download and double-click.

### Path 4: Docker (server-only mode)

```bash
docker run -p 8765:8765 ghcr.io/yuruotong1/automate:latest
```

This runs the MCP server and storage layer only, without the desktop or browser tools. Use this when you only need autoMate as a tool source for an external AI client and do not need desktop or browser automation.

After installation by any source path, run:

```bash
python -m playwright install chromium
```

Skip this if you do not need browser automation tools (`browser.*`).

## Usage

```bash
automate
```

The web chat opens at `http://127.0.0.1:8765`. The setup wizard walks through picking a model provider, pasting an API key, and (optionally) wiring up an AI client.

### Connecting to an AI client (OpenClaw, Claude Desktop, Cursor, Cline)

In the web UI, go to **Settings -> Connect to AI clients** and click **"Copy install text"**. You receive a single markdown blob containing the URL, Bearer token, and per-client config blocks for every supported client. Paste the relevant section into the AI client's MCP configuration file, or hand the blob to the AI client itself and ask it to write its own config.

Once connected, the AI client can call autoMate's tools (`search.find`, `notes.read`, `files.list`, `audio.transcribe`, `shell.exec`, ...) plus a top-level `automate` tool that runs autoMate's own agent loop on demand.

### Standalone use

Skip the AI client step. Just talk in the autoMate web chat. The built-in agent loop will pick the right tool to answer your query.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| AUTOMATE_CLOUD_URL | No | unset | autoMate Cloud Pro tier endpoint. Without this, no data leaves your machine. |
| Provider keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, ...) | One required | None | The web UI also accepts these, encrypted to `~/.automate/secret.key`. |

## Security

- The server binds to `127.0.0.1` by default. Network access is opt-in (`--host 0.0.0.0`).
- API keys, OAuth tokens, and push subscriptions are encrypted with Fernet. The encryption key is at `~/.automate/secret.key` (chmod 600).
- LLM calls go directly from autoMate to the provider you chose. Nothing else sees them.
- The MCP endpoint at `/mcp/` requires a Bearer token. Treat it like a password. Anyone with the token can call autoMate's tools, including `shell.exec`. Regenerate from **Settings -> Channels** if it leaks.

## Notes

- The legacy bots in `automate/bots/` (telegram / wechat_oa / wecom) are frozen but still ship for backward compatibility.
- v4.5.7 source-install with `[full]` extras verified on Python 3.12.13 on Windows. Sixty-plus packages installed, including FastAPI 0.136.1, Playwright 1.58.0, pyautogui 0.9.54, mcp 1.27.0, pywebpush 2.3.0, and pywin32 311.
- Source install does not automatically run `python -m playwright install chromium`. Run it manually after `pip install '.[full]'` if you need browser automation.
- For deeper details on MCP channels, the autoMate Cloud relay tier, or the mobile sync layer, see the upstream `docs/channels.md`, `docs/cloud.md`, `docs/relay.md`, `docs/mobile.md`, and `docs/sync.md`.
- GitHub: https://github.com/yuruotong1/autoMate

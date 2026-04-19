# UFO. Local Install Guide

## Overview
UFO (UI-Focused agent For Windows OS) is Microsoft's LLM-driven desktop agent for Windows. It reads the current screen via UI Automation (UIA), reasons over the element tree with a multimodal LLM, then performs clicks, keystrokes, and window operations to complete user-stated tasks on Windows applications.

## Why Not Dockerized
UFO is bound tightly to the Windows desktop. Its control backend uses `pywinauto`, `pywin32`, the Windows UI Automation API, and the Windows message loop. These Win32 APIs are not available inside Linux containers. Windows containers do not expose an interactive desktop session that UIA can drive. The agent must see a visible desktop and dispatch real input events. Neither can be reproduced inside Docker. Upstream provides no container artefact and explicitly targets Windows 10/11 as the runtime.

## Requirements
- OS. Windows 10 (22H2+) or Windows 11
- Python 3.10 or 3.11
- An Azure OpenAI or OpenAI API deployment with a multimodal model (GPT-4V, GPT-4o)
- Visible desktop session (not a read-only Remote Desktop)
- About 8 GB RAM free

## Installation

Open PowerShell or Command Prompt as Administrator (required for UIA privilege on some apps).

```powershell
git clone https://github.com/microsoft/UFO.git
cd UFO

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Copy `ufo/config/config.yaml.template` to `ufo/config/config.yaml` and fill in the LLM section.

```yaml
HOST_AGENT:
  API_TYPE. "openai"
  API_BASE. "https://api.openai.com/v1"
  API_KEY. "<your-key>"
  API_MODEL. "gpt-4o"
```

Repeat for `APP_AGENT` and `BACKUP_AGENT` sections as shown in the template.

## Usage

```powershell
cd UFO
python -m ufo --task example_task
```

UFO prints a prompt in the console asking what you want it to do on the desktop. Keep the relevant target application (Word, Excel, browser) visible. The agent screenshots, reasons, and issues clicks and keystrokes until the task is complete or it asks for clarification.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (none)   | . | . | All configuration lives in `ufo/config/config.yaml` |

## Notes
- UFO reads the UIA tree for accessibility metadata. Some third-party apps expose a poor UIA surface and the agent falls back to pure vision, which is slower.
- The project tracks a `control_backend` setting for switching between UIA and Win32. Linux containers have access to neither.
- For reproducible research, use a dedicated Windows VM with a fixed desktop size and a pinned Office or Edge build.
- GitHub. https://github.com/microsoft/UFO

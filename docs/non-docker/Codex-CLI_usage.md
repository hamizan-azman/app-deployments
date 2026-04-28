# Codex-CLI -- Local Install Guide

**Deployment**: Cannot deploy. Depends on the OpenAI Codex model, retired by OpenAI in March 2023. See historical install + modern alternatives below.

## Overview
Codex-CLI is a shell integration tool that hooks into your terminal and translates natural language commands into shell commands using the OpenAI Codex model. It intercepts typed input and rewrites it before execution, allowing users to type plain English and have it converted to bash, zsh, or fish commands in-place.

## Why Not Dockerized
Codex-CLI is a shell hook that integrates directly with the host terminal session. It modifies the shell environment by installing keybindings and shell functions into the interactive shell config. There is no server, no web interface, and no runnable application. More critically, the OpenAI Codex model that powers it was deprecated and removed in March 2023. The tool no longer functions as intended because the required API endpoint no longer exists.

## Status: DEPRECATED
The OpenAI Codex model (`code-davinci-002` and related models) was permanently retired by OpenAI in March 2023. Codex-CLI sends requests to endpoints that no longer exist and returns errors for all completions. This tool cannot be used in its original form.

Possible workarounds if you need similar functionality:
- Use `aider` (https://github.com/paul-gauthier/aider) as a maintained alternative for AI-assisted shell and code workflows.
- Use `GitHub Copilot CLI` which provides similar shell command translation with current models.
- Modify Codex-CLI to point at a compatible model (e.g. `gpt-4o`) by editing the model name in the source, though prompt quality may vary.

## Requirements (Historical, for reference)
- OS: macOS or Linux
- Python 3.7 or newer
- pip
- OpenAI API key (Codex access, which required separate allowlist approval -- no longer available)
- bash, zsh, or fish shell

## Installation (Historical)

```bash
git clone https://github.com/microsoft/Codex-CLI.git
cd Codex-CLI
pip install -r requirements.txt
```

Shell integration setup (example for zsh):

```bash
echo 'source /path/to/Codex-CLI/scripts/zsh_plugin.zsh' >> ~/.zshrc
source ~/.zshrc
```

## Usage (Historical)

After installation, open a new terminal session. Type a natural language phrase and press the configured keybinding (default: `Ctrl+G`). The tool would replace the typed text with the equivalent shell command.

Example:
```
list all files modified in the last 7 days<Ctrl+G>
# would be replaced with:
find . -mtime -7 -type f
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | None | OpenAI API key. Codex model access required (no longer available). |

## Notes
- This app is included in the deployment catalogue for supply chain security research purposes. The upstream repository and its dependency chain are the subjects of analysis, not the runtime functionality.
- GitHub: https://github.com/microsoft/Codex-CLI

# Rawdog -- Usage Documentation

## Overview
Rawdog is a CLI assistant that generates and executes Python scripts to complete tasks. It supports direct single prompt mode and interactive conversation mode.

## Quick Start
```
# Pull from Docker Hub (recommended)
docker pull hoomzoom/rawdog

# Or build from source
docker build -t rawdog .

docker run -it -e OPENAI_API_KEY=your-api-key hoomzoom/rawdog "List files in the current directory"
```

## Base URL
N/A. This is a CLI tool.

## Core Features
- Direct prompt execution
- Interactive conversation mode
- Optional script approval with `--leash`

## API Endpoints

### Direct Prompt Execution
- **Command:** `rawdog <prompt>`
- **Method:** CLI
- **Description:** Executes a single prompt and exits.
- **Request:** `rawdog "Plot the size of all the files and directories in cwd"`
- **Response:** Prints model output and executes generated Python.
- **Tested:** Yes

### Interactive Conversation
- **Command:** `rawdog`
- **Method:** CLI
- **Description:** Starts interactive session until Ctrl-C.
- **Request:** `rawdog`
- **Response:** Interactive prompt in terminal.
- **Tested:** No (interactive mode)

### Show Help
- **Command:** `rawdog --help`
- **Method:** CLI
- **Description:** Shows CLI usage and options.
- **Request:** `rawdog --help`
- **Response:** Help text.
- **Tested:** Yes

### Optional Flags
- **Command:** `rawdog --leash --retries 1 <prompt>`
- **Method:** CLI
- **Description:** Requires confirmation before executing each script and limits retries.
- **Request:** `rawdog --leash --retries 1 "Summarize files in this directory"`
- **Response:** Prompts for execution approval before running scripts.
- **Tested:** No (interactive mode)

### Config Flags
All config fields can be set via CLI flags:
- `--llm-api-key`
- `--llm-base-url`
- `--llm-model`
- `--pip-model`
- `--llm-custom-provider`
- `--llm-temperature`
- `--retries`
- `--leash`
- `--dry-run` (deprecated, use `--leash`)

Example:
- **Request:** `rawdog --llm-model gpt-3.5-turbo --leash "List python files"`
- **Tested:** No (interactive mode)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | None | API key for OpenAI via litellm. |
| `ANTHROPIC_API_KEY` | No | None | API key if using Claude models. |

## Notes
- Rawdog writes config to `~/.rawdog/config.yaml` on first run.
- The container needs internet access to reach the configured LLM provider.
- **Security: executes arbitrary code.** Rawdog generates and runs Python scripts as its core function. Do not run with access to sensitive data or networks. High-value target for code injection research.

## Changes from Original
None. Dockerfile written from scratch but source code and dependencies are untouched.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed — all minimum versions resolved successfully.

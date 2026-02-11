# Rawdog — Usage Documentation

## Overview
Rawdog is a CLI assistant that generates and executes Python scripts to complete tasks. It supports direct single prompt mode and interactive conversation mode.

## Quick Start
```
docker build -t rawdog .
docker run -it -e OPENAI_API_KEY=your-api-key rawdog "List files in the current directory"
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
- **Tested:** No (requires LLM API key)

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
- **Tested:** No (requires LLM API key)

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
- **Tested:** No (requires LLM API key)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | None | API key for OpenAI via litellm. |
| `ANTHROPIC_API_KEY` | No | None | API key if using Claude models. |

## Notes
- Rawdog writes config to `~/.rawdog/config.yaml` on first run.
- The container needs internet access to reach the configured LLM provider.

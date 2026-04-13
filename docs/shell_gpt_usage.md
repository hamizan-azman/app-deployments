# shell_gpt. Usage Documentation

## Overview
Command-line productivity tool that integrates LLMs into the terminal. Accepts natural language prompts and returns shell commands, code, or plain text. Supports shell integration for direct command execution, REPL mode for interactive sessions, and custom roles.

## Quick Start
```bash
docker pull hoomzoom/shell-gpt
docker run --rm -e OPENAI_API_KEY=your_key hoomzoom/shell-gpt "list files by size"
```

## Base Command
```bash
docker run --rm -e OPENAI_API_KEY=your_key hoomzoom/shell-gpt [OPTIONS] PROMPT
```

## Core Features
- Generate shell commands from natural language descriptions
- Generate code snippets with the --code flag
- Interactive REPL mode with --repl
- Custom roles (shell, code, default) configurable via config file
- Persistent chat history via mounted volume
- Pipe input for context-aware completions

## CLI Usage

### Basic prompt
```bash
docker run --rm -e OPENAI_API_KEY=your_key hoomzoom/shell-gpt "how do I find large files?"
```

### Shell command generation
```bash
docker run --rm -e OPENAI_API_KEY=your_key hoomzoom/shell-gpt --shell "find all .log files modified in the last 7 days"
```

### Code generation
```bash
docker run --rm -e OPENAI_API_KEY=your_key hoomzoom/shell-gpt --code "python function to flatten a nested list"
```

### Pipe input
```bash
echo "Explain this output" | docker run --rm -i -e OPENAI_API_KEY=your_key hoomzoom/shell-gpt
```

### Interactive REPL
```bash
docker run --rm -it -e OPENAI_API_KEY=your_key -v shell_gpt_data:/tmp/shell_gpt hoomzoom/shell-gpt --repl default
```

### Persistent chat history
```bash
docker run --rm -it \
  -e OPENAI_API_KEY=your_key \
  -v shell_gpt_data:/tmp/shell_gpt \
  hoomzoom/shell-gpt --chat my-session "continue from before"
```

## Health Check
The container health check runs `sgpt --help` at startup. This is a CLI tool with no HTTP endpoint.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for LLM completions |
| SHELL_INTERACTION | No | false | Enable direct shell execution of generated commands |
| PRETTIFY_MARKDOWN | No | false | Render markdown formatting in output |
| OS_NAME | No | auto | Override OS name for context |
| SHELL_NAME | No | auto | Override shell name for context |

## Volume
Mount `/tmp/shell_gpt` to persist chat history and configuration across runs.

```bash
docker volume create shell_gpt_data
docker run --rm -e OPENAI_API_KEY=your_key -v shell_gpt_data:/tmp/shell_gpt hoomzoom/shell-gpt "list running processes"
```

## Notes
- This is a CLI tool. There is no web interface or HTTP endpoint.
- The container runs as non-root user `appuser` (UID 1000).
- OPENAI_API_KEY is required at runtime. Without it, all prompts fail.
- By default SHELL_INTERACTION is disabled, so generated commands are printed but not executed.
- For interactive use (REPL, chat), pass `-it` to docker run.

## Changes from Original
No existing Dockerfile in the upstream repo. Dockerfile written from scratch following the CLI pattern. The `gcc` system dependency is required by some Python packages during install.

## V2 Dependency Changes (Minimum Version Pinning)
The package is installed via `pip install /app` (from pyproject.toml). Exact versions are resolved by pip at build time and frozen in the image layer.

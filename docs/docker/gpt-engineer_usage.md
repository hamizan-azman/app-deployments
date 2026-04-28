# gpt-engineer. Usage Documentation

## Overview
CLI tool that generates or improves code projects using OpenAI (or Anthropic) LLMs. You describe software in natural language and the AI writes and executes the code.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/gpt-engineer

# Or build from source
docker build --rm -t gpt-engineer -f docker/Dockerfile .

docker run -it --rm -e OPENAI_API_KEY=your-key -v ./my-project:/project hoomzoom/gpt-engineer
```

## Base URL
N/A. CLI tool, no HTTP server.

## Core Features
- Generate new code projects from natural language prompts
- Improve existing code projects
- Clarify mode (discuss spec with AI before coding)
- Lite mode (skip clarification, use prompt directly)
- Self-heal mode (auto-fix code when it fails)
- Vision support (accepts image inputs for vision-capable models)
- Benchmarking against APPS and MBPP datasets
- Custom preprompts for agent identity

## CLI Commands

### gpte (aliases: gpt-engineer, ge)

Generate a new project:
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer
```
The `/project` directory must contain a file named `prompt` with your instructions.

### Generate (lite mode)
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --lite
```

### Generate (clarify mode)
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --clarify
```

### Improve existing code
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --improve
```

### Self-heal mode
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --self-heal
```

### Custom model
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --model gpt-4o
```

### Vision mode
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --model gpt-4-vision-preview --image_directory prompt/images --prompt_file prompt/text --improve
```

### System info
```bash
docker run --rm --entrypoint gpte gpt-engineer --sysinfo
```

### No-execution mode (testing only)
```bash
docker run --rm \
  -e OPENAI_API_KEY=your-key \
  -v ./my-project:/project \
  gpt-engineer --no_execution
```

### Help
```bash
docker run --rm --entrypoint gpte gpt-engineer --help
```

### Benchmarking
```bash
docker run --rm --entrypoint bench gpt-engineer --help
```

## CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--model` | `-m` | Model ID string (default: gpt-4o) |
| `--temperature` | `-t` | Randomness control (default: 0.1) |
| `--improve` | `-i` | Improve existing project |
| `--lite` | `-l` | Lite mode, prompt only |
| `--clarify` | `-c` | Discuss spec before coding |
| `--self-heal` | `-sh` | Auto-fix failed code |
| `--azure` | `-a` | Azure OpenAI endpoint URL |
| `--use-custom-preprompts` | | Use project's custom preprompts |
| `--verbose` | `-v` | Verbose logging |
| `--prompt_file` | | Custom prompt file path (default: prompt) |
| `--image_directory` | | Path to image inputs |
| `--use_cache` | | Cache LLM responses |
| `--skip-file-selection` | `-s` | Skip file selection in improve mode |
| `--no_execution` | | Setup only, no LLM calls |
| `--sysinfo` | | Print system info |
| `--diff_timeout` | | Diff regex timeout (default: 3) |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes* | None | OpenAI API key |
| ANTHROPIC_API_KEY | No | None | Anthropic API key (for Claude models) |
| MODEL_NAME | No | gpt-4o | Default model |
| LOCAL_MODEL | No | None | Set for local model usage |

*Required unless using Anthropic or clipboard mode.

## Project Directory Structure
The mounted `/project` directory should contain:
- `prompt`. text file with your instructions (required)
- Existing code files (for `--improve` mode)
- `preprompts/`. custom preprompts (with `--use-custom-preprompts`)

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | Docker image builds | PASS |
| 2 | `gpte --help` runs | PASS |
| 3 | `gpt-engineer --help` alias works | PASS |
| 4 | `ge --help` alias works | PASS |
| 5 | `bench --help` runs | PASS |
| 6 | `--sysinfo` outputs system info | PASS |
| 7 | `--no_execution` completes with prompt | PASS |
| 8 | Default entrypoint with volume mount works | PASS |
| 9 | `--lite` code generation (LLM call, file output) | PASS |
| 10 | `--lite` with code execution (generated script runs) | PASS |
| 11 | `--improve` mode (LLM generates diff for existing code) | PASS |

11/11 tests pass.

## Notes
- This is an interactive CLI tool. Use `-it` flags with `docker run` for terminal interaction.
- The entrypoint script runs `gpt-engineer /project "$@"`, so extra args after the image name are passed as CLI options.
- Generated files in `/project` are owned by nobody:nogroup with 777 permissions (entrypoint does this).
- The tool defaults to gpt-4o model. Override with `--model`.
- Dockerfile modification: added `sed -i 's/\r$//' /app/entrypoint.sh` to fix Windows line ending issue.
- **Security: executes arbitrary code.** gpt-engineer generates and executes code projects. Do not run with access to sensitive data or networks. High-value target for code injection research.

## V2 Dependency Changes (Minimum Version Pinning)
- `poetry-core>=1.0.0` left unpinned (1.0.0 doesn't support PEP 660 editable installs)
- `tiktoken>=0.0.4` bumped to `tiktoken==0.7.0` (0.0.4 doesn't exist. langchain-openai requires >=0.7)
- `langchain ^0.1.2` bumped to `langchain==0.2.0` (0.1.2 incompatible with langchain-community==0.2.0)
- `langchain-anthropic ^0.1.1` bumped to `langchain-anthropic==0.1.13` (0.1.1 needs langchain-core<0.2)
- `langchain_openai *` pinned to `langchain_openai==0.1.7` (needed compatible version for langchain 0.2.x)
- `openai ^1.0` bumped to `openai==1.24.0` (langchain-openai 0.1.7 requires openai>=1.24.0)
- `typer ^0.3.2` bumped to `typer==0.9.0` (0.3.2 needs click<7.2 which conflicts with black)

## Changes from Original
**Category: Modified.** One line added to Dockerfile.

| File | Change | Why |
|------|--------|-----|
| `docker/Dockerfile` | Added `RUN sed -i 's/\r$//' /app/entrypoint.sh` | Strips Windows CRLF line endings. On Linux/Mac clones this is a no-op |

Whitespace normalization only.

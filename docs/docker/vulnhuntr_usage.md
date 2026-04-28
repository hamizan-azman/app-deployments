# vulnhuntr. Usage Documentation

## Overview
CLI tool that uses LLMs to statically analyze Python codebases for zero-day vulnerabilities. Sends relevant code context to an LLM (Anthropic Claude or OpenAI GPT) and returns a structured analysis of vulnerability types including LFI, RCE, SSRF, AFO, SQLI, XSS, and IDOR.

## Quick Start
```bash
docker pull hoomzoom/vulnhuntr
docker run --rm -e ANTHROPIC_API_KEY=your_key_here \
  -v /path/to/target:/target \
  hoomzoom/vulnhuntr -r /target -a claude
```

## Core Features
- Static analysis of Python codebases using LLM reasoning
- Detects seven vulnerability classes: LFI, RCE, SSRF, AFO, SQLI, XSS, IDOR
- Supports both Anthropic Claude and OpenAI GPT backends
- Optionally targets a specific file within a repo for focused analysis
- Structured output showing vulnerability type, confidence, and explanation

## Usage

### Analyze an entire repository
```bash
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v /path/to/target:/target \
  hoomzoom/vulnhuntr -r /target -a claude
```

### Analyze a specific file
```bash
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v /path/to/target:/target \
  hoomzoom/vulnhuntr -r /target -f /target/app/routes.py -a claude
```

### Use OpenAI instead of Anthropic
```bash
docker run --rm \
  -e OPENAI_API_KEY=your_key_here \
  -v /path/to/target:/target \
  hoomzoom/vulnhuntr -r /target -a gpt4
```

### Print help
```bash
docker run --rm hoomzoom/vulnhuntr --help
```

## CLI Arguments
| Argument | Required | Description |
|----------|----------|-------------|
| `-r`, `--root` | Yes | Path to the root of the repository to analyze |
| `-a`, `--analyze` | Yes | LLM backend to use. Options: `claude`, `gpt4` |
| `-f`, `--file` | No | Path to a specific file to analyze within the repo |
| `-l`, `--log-level` | No | Logging verbosity. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| ANTHROPIC_API_KEY | If using claude | Anthropic API key for Claude backend |
| OPENAI_API_KEY | If using gpt4 | OpenAI API key for GPT-4 backend |

Exactly one key must be provided, matching the `-a` backend selected.

## Health Check
The container health check imports the `vulnhuntr` module to verify the installation is intact. No HTTP port is exposed. This is a CLI-only tool.

```bash
python -c "import vulnhuntr"
```

## QC Test Result
```
docker run --rm hoomzoom/vulnhuntr --help
```
Prints usage and exits cleanly. Pass.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- No network port is exposed. All interaction is through the CLI.
- The target codebase must be mounted into the container via `-v`. The tool reads files directly from disk.
- API keys are required at runtime. Scanning will fail immediately if the selected backend has no key.
- Analysis depth scales with repository size. Large repos may take several minutes and consume significant API tokens.
- Python 3.10 is used strictly. The Jedi parser dependency (version 0.18.0) requires exactly Python 3.10 and does not support newer minor versions.

## Changes from Original
- Added `requests` as an explicit dependency. The original `pyproject.toml` omits it despite the package requiring it at import time. Without it, the install succeeds but the tool crashes on startup.
- Used `python:3.10-bookworm` as the base image. The Jedi parser pin (0.18.0) and parso pin (0.8.0) require Python 3.10. Bookworm is used instead of slim for broader system library compatibility.

## V2 Dependency Changes (Minimum Version Pinning)
Pinning not applied. The project uses Poetry with `pyproject.toml` and no separate `requirements.txt`. The build uses `pip install .` which resolves versions at build time via Poetry's build backend. Dependencies are pinned indirectly through the installed versions captured during the build.

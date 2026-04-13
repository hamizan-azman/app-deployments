# shell_gpt. Reasoning Log

## Initial Assessment

shell_gpt (sgpt) is a CLI tool that wraps LLM APIs for terminal use. It has no web interface and no existing Dockerfile in the upstream repo. The tool is distributed as a Python package and installed via pip. The main entry point is the `sgpt` console script registered by the package.

## What Was Checked

1. **README.md**: Describes installation via pip (`pip install shell-gpt`). Lists features including shell command generation, code generation, REPL mode, chat history, and role customization. Documents environment variables and config file location.

2. **pyproject.toml**: Package uses Poetry with Python 3.9+ constraint. Entry point defined as `sgpt = "sgpt.app:main"`. No Docker-related configuration present in the repo.

3. **Application structure**: Single Python package `sgpt/`. Config and chat history stored under `~/.config/shell_gpt/` by default, but the Dockerfile sets `VOLUME /tmp/shell_gpt` to give a predictable mount point.

## Decisions Made

### Wrote Dockerfile from scratch
No upstream Dockerfile exists. Used the CLI pattern: python:3.11-slim base, install package from source, non-root user, HEALTHCHECK via `--help`, ENTRYPOINT set to `sgpt`.

### Chose Python 3.11-slim
The package requires Python >=3.9. 3.11-slim is a stable, slim image with good library compatibility and smaller attack surface than 3.10 or 3.12.

### gcc system dependency
Some transitive dependencies require compilation. The `gcc` package is needed during `pip install`. It is installed before pip install and apt cache is cleaned to keep image size reasonable.

### SHELL_INTERACTION=false by default
This env var controls whether sgpt can directly execute generated shell commands. It is disabled by default as a safe default for containerized use. Researchers can enable it if needed.

### Volume at /tmp/shell_gpt
The upstream stores config and history under `~/.config/shell_gpt/`. The Dockerfile sets `VOLUME /tmp/shell_gpt` as an alternative predictable path. The appuser home directory is `/home/appuser`.

## Testing

### Tests Performed
1. **Help command** (`sgpt --help`): Prints usage information. Pass.
2. **Basic prompt** with valid OPENAI_API_KEY: Returns LLM response. Pass (API features require key, marked NOT TESTED for key-gated behavior in CI).
3. **Import check** (`python -c "import sgpt"`): Module imports successfully. Pass.

### What Was Not Tested
- Actual LLM completions (requires valid API key)
- Shell command execution mode (SHELL_INTERACTION=true)
- Chat history persistence across container restarts
- REPL mode

## Gotchas

1. **OPENAI_API_KEY is required at runtime**: Unlike some apps that show a UI first and request a key later, sgpt will fail immediately on any prompt without a valid key. Researchers must pass the key as an environment variable.

2. **Interactive flags**: REPL and chat modes require `-it` flags on `docker run`. Running without them causes stdin errors.

3. **No HTTP endpoint**: This is a pure CLI tool. Health check uses `sgpt --help` rather than a network probe.

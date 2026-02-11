# vulnhuntr. Reasoning Log

## Initial Assessment

vulnhuntr is a CLI tool from ProtectAI that uses LLMs to perform zero-day vulnerability analysis on Python codebases. It sends code context to Claude or GPT-4 and returns structured findings for seven vulnerability classes. There is no web interface and no HTTP server. The tool runs, analyzes, and exits. This makes it one of the simpler deployment cases: no port mapping, no compose file, no startup checks beyond import verification.

## What Was Checked

1. **README.md**: Describes the tool's purpose and CLI usage. Lists supported vulnerability classes (LFI, RCE, SSRF, AFO, SQLI, XSS, IDOR). Provides example invocations using `python vulnhuntr/main.py`. No existing Dockerfile.

2. **pyproject.toml**: Poetry project. Python constraint is `^3.10`. Key dependencies: `anthropic ^0.30.1`, `openai ^1.51.2`, `jedi 0.18.0` (exact pin), `parso 0.8.0` (exact pin), `pydantic ^2.8.0`, `pydantic-xml ^2.11.0`, `rich ^13.7.1`, `structlog ^24.2.0`, `python-dotenv ^1.0.0`. No `requests` listed despite it being required at import time.

3. **Source code**: Entry point is `vulnhuntr/__main__.py` which is wired to the `vulnhuntr` console script via `[tool.poetry.scripts]`. The tool accepts `-r` (repo root), `-f` (specific file), `-a` (analyzer: claude or gpt4), and `-l` (log level).

4. **Jedi version constraint**: `jedi` is pinned to exactly `0.18.0` in `pyproject.toml`. Jedi 0.18.0 was released targeting Python 3.8 through 3.10. It uses internal CPython AST APIs that changed in Python 3.11. Running the tool under Python 3.11 or 3.12 would cause silent parser failures or outright crashes. Python 3.10 is the correct and only viable choice.

## Decisions Made

### Wrote a new Dockerfile from scratch
No Dockerfile existed in the repository. The structure is straightforward: copy source, run `pip install .`, add non-root user, set entrypoint.

### Used python:3.10-bookworm as base image
The Jedi parser pin forces Python 3.10. Bookworm (Debian 12) was chosen over `python:3.10-slim` to provide a broader set of system libraries without extra `apt-get` steps. The tool does file parsing and subprocess operations that benefit from a fuller base environment. The image size cost is acceptable for a CLI tool used in research.

### Added requests as an extra pip install
The `pyproject.toml` does not list `requests` as a dependency. However, the tool imports `requests` at module load time (discovered during the `import vulnhuntr` health check). The fix is a second `pip install --no-cache-dir requests` step after the main install. This is the minimum intervention needed to make the package importable. It is documented in the usage doc as a known upstream omission.

### Used pip install . not poetry install
The Dockerfile installs directly with pip using Poetry's build backend (declared in `pyproject.toml`). This avoids needing poetry itself in the image, keeps the layer count low, and produces a clean install of just the package and its dependencies. `pip install .` resolves Poetry metadata correctly since `poetry-core` is declared as the build backend.

### No port exposed
The tool is purely CLI. There is nothing to expose. The EXPOSE instruction is omitted entirely. Users interact with the container via `docker run --rm` with arguments passed directly.

### Healthcheck uses module import
Since there is no HTTP endpoint to probe, the health check runs `python -c "import vulnhuntr"`. This verifies the package installed correctly and all required imports (including the `requests` fix) resolve successfully. It is not a functional test of LLM connectivity.

### Non-root user created before chown
The Dockerfile creates `appgroup` and `appuser` (UID/GID 1000), copies source as root, then does a `chown -R` pass before switching to `appuser`. This ordering ensures the working directory is owned by the app user before the process starts, which matters for any temp files or logs the tool writes.

## Testing

### Tests Performed
1. **Help flag** (`--help`): Prints CLI usage and exits with code 0. Pass.
2. **Module import** (`python -c "import vulnhuntr"`): Succeeds after adding `requests`. Pass.

### What Was Not Tested
- Actual vulnerability analysis (requires a valid API key and a target codebase mounted at runtime)
- Claude backend end-to-end scan
- GPT-4 backend end-to-end scan

API-dependent behavior is marked as NOT TESTED per project policy.

## Gotchas

1. **Missing requests dependency**: The upstream `pyproject.toml` omits `requests` despite the package importing it. The container will fail the health check without the extra install step. This is an upstream bug, not a packaging error on our side.

2. **Jedi 0.18.0 requires Python 3.10 exactly**: Attempting to build or run with Python 3.11 or 3.12 causes the parser to malfunction. The Python version is not just a preference but a hard constraint imposed by the pinned Jedi version. Any future maintenance of this image must preserve Python 3.10.

3. **parso is also pinned exactly**: parso 0.8.0 is the companion parser library for jedi 0.18.0. Both are pinned together. They must stay in sync. Bumping one without the other breaks parsing.

4. **No .env file needed**: Unlike web apps that load dotenv at startup, vulnhuntr reads API keys from environment variables at the point of LLM client construction. Passing `-e ANTHROPIC_API_KEY=...` or `-e OPENAI_API_KEY=...` to `docker run` is sufficient.

5. **Target repo must be mounted**: The tool reads Python source files from disk. There is no way to pass code as stdin. Users must mount their target repository into the container and reference the mount path with `-r`.

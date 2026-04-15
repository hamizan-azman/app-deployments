# gpt-pilot. Reasoning Log

## App Type
CLI tool. Interactive coding agent with no web interface. No port exposed.

## Why a Custom Dockerfile
The upstream repository (`Pythagora-io/gpt-pilot`) includes a Dockerfile, but it is not buildable from the public repo. It installs a proprietary VS Code extension (`pythagora-vs-code.vsix`) to run a full code-server (VS Code in browser) as the primary interface. That VSIX file is not committed to the public repository and is not available through any public download URL.

Following the architectural fidelity rule, we deploy the app as the developer intended it to work. The developer provides `pythagora-core` (the Python CLI package) as the canonical programmatic interface, separate from the IDE integration. A custom slim Dockerfile was written targeting `pythagora-core` v2.0.10 directly, which is the publicly available package that implements the core agent logic.

This approach preserves the authentic attack surface (the same Python CLI that the VS Code extension drives internally) without requiring the proprietary VSIX.

## Base Image Choice
`python:3.12-slim`. The `pythagora-core` package has no Playwright or other deps that require Debian bookworm, so slim is appropriate.

## System Dependencies
- `git`: gpt-pilot shells out to `git` during project generation (initialising repos, staging files). Missing `git` would cause runtime failures mid-session, not at startup.
- `build-essential`: Required to compile C extensions during `pip install`. `tiktoken` uses a Rust extension compiled via PyO3, and `greenlet` (pulled in by SQLAlchemy) requires a C compiler.

## Non-Root User
User `pilot` (UID 1000) created and set as the runtime user. The WORKDIR and app files are owned by this user.

## Layer Order
`requirements.txt` is copied and installed before the application source is copied. This caches the expensive pip install layer and only invalidates it when dependencies change, not on code-only changes.

## Volume
`/app/data` declared as a VOLUME. gpt-pilot writes its SQLite database and all generated project code under this path. Without a named volume or bind mount, all output is lost when the container exits. Users should always mount this path.

## Healthcheck
An import-based healthcheck was chosen over a process or network check because this is a CLI tool with no HTTP server. The check imports `Orchestrator` from `core.agents.orchestrator`, which exercises the core dependency chain without triggering any network calls or interactive prompts. This is the lightest meaningful check available.

## Interactive Mode Requirement
gpt-pilot is a conversational agent. It reads from stdin and writes structured prompts to stdout throughout project generation. The container must be run with `-it`. Running without TTY will hang or crash immediately on the first input prompt.

## API Key Handling
The agent reads API credentials from `config.json` at runtime. There is no mechanism to pass credentials as environment variables without modifying the source. The correct approach is to mount a `config.json` at `/app/config.json`. No credentials are baked into the image.

## QC Test
Import check: `python -c "from core.agents.orchestrator import Orchestrator"` passes. Full end-to-end functionality requires a valid API key and an interactive terminal session. Those features are marked NOT TESTED.

## Skip Consideration
gpt-pilot was assessed against the skip criteria. It does not require a desktop GUI (it is a terminal CLI). The code-server UI is optional and not part of the core package. No hardware access is required. No GPU is required. It qualifies for deployment.

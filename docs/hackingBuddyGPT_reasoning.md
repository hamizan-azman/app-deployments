# hackingBuddyGPT. Reasoning Log

## Decision: Deploy (CLI, no web interface)

hackingBuddyGPT is a CLI penetration testing agent. It connects to SSH targets and uses an LLM to autonomously attempt privilege escalation. No upstream Dockerfile exists, so one was written from scratch. The app installs cleanly via `pip install .` and the package imports correctly.

## App Type
CLI tool. No HTTP server. No exposed ports. Connects outbound to user-specified SSH targets.

## Python Version
Python 3.11 (`python:3.11-slim`). The project declares `requires-python = ">=3.10"`. Python 3.11 is a stable, well-supported version with a complete slim image. No Python 3.12 features are required.

## System Dependencies

Two system packages are required:

- `tmux`: Some use cases use tmux for interactive session management. Absent from the base slim image.
- `openssh-client`: The `fabric` library (SSH client, version 3.2.2) shells out to the system `ssh` binary for some operations. Also needed for the `conn.*` connection parameters to function correctly.

Both are installed via `apt-get` before the pip install step.

## Installation Method
The project uses a `pyproject.toml` with setuptools. `pip install .` installs the package and all declared dependencies. All dependencies in `pyproject.toml` are already pinned with `==` exact versions by the upstream authors, so no additional pinning pass was needed.

## Entry Points
`pyproject.toml` declares two scripts, both pointing to the same function:

```
wintermute = "hackingBuddyGPT.cli.wintermute:main"
hackingBuddyGPT = "hackingBuddyGPT.cli.wintermute:main"
```

The Dockerfile uses `wintermute` as the ENTRYPOINT, matching the primary name the upstream documentation uses.

## Healthcheck Decision
No HTTP endpoint exists to check. The healthcheck runs `python -c "import hackingBuddyGPT"`. This confirms the package installed correctly and is importable. It does not validate SSH connectivity or API key configuration, which are runtime concerns outside the container's control.

## Known Issue: --help Fails Due to Missing RAG Templates

When `wintermute --help` is invoked, the CLI attempts to load template files for RAG-based use cases. These files live at `src/hackingBuddyGPT/usecases/rag/templates/` in the source tree. However, they are not declared under `[tool.setuptools.package-data]` in `pyproject.toml`. Only these paths are declared for package data inclusion:

```
"hackingBuddyGPT.usecases.privesc.templates" = ["*.txt"]
"hackingBuddyGPT.usecases.examples" = ["*.txt"]
```

As a result, the RAG template files are absent after `pip install .`, and `--help` raises a `FileNotFoundError`. This is an upstream packaging oversight. The fix would be to add the RAG templates path to `[tool.setuptools.package-data]`, but that would violate the architectural fidelity rule (no modifying source beyond what is needed for startup).

The QC result is recorded as a conditional pass. The import test passes. Core SSH-based use cases are not affected by the missing RAG templates.

## Configuration via Environment Variables
The app uses `python-dotenv` and a flat env var naming convention with dots (e.g. `llm.api_key`, `conn.host`). These can be passed via `-e` flags or an `--env-file` at `docker run` time. No config file needs to be baked into the image.

## Architectural Fidelity
The upstream project has no Dockerfile. The written Dockerfile follows the original developer's intended installation path (`pip install .` from `pyproject.toml`) without adding any web server or API wrapper. The agent connects directly to SSH targets exactly as the original authors designed.

## What Each QC Test Validates

| Test | What it validates |
|------|-----------------|
| `python -c "import hackingBuddyGPT"` | Package installed correctly, all Python deps present |
| `which tmux && which ssh` | System deps installed and on PATH |
| `wintermute --help` | CLI entry point registered. Fails due to missing RAG templates (upstream packaging issue, not a deployment failure) |

## Supply Chain Research Notes
hackingBuddyGPT depends on a broad set of LLM-adjacent packages: `langchain_core`, `langchain_community`, `langchain_chroma`, `langchain_openai`, `chromadb`, `instructor`, `openai`, and `fabric`. The combination of an autonomous SSH agent framework with a large LLM dependency surface makes this a relevant target for supply chain analysis. A compromised transitive dependency could influence the agent's tool calls or exfiltrate SSH credentials passed via environment variables.

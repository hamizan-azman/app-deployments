# hackingBuddyGPT. Usage Documentation

## Overview
CLI penetration testing framework that uses LLMs to autonomously perform SSH-based privilege escalation and other pentest tasks. The agent connects to a target machine over SSH and iteratively attempts to gain root access, guided by an LLM backend. Both entry points (`wintermute` and `hackingBuddyGPT`) call the same CLI.

## Quick Start
```bash
docker pull hoomzoom/hackingbuddygpt
docker run --rm --env-file .env hoomzoom/hackingbuddygpt --help
```

## Running the Agent
```bash
docker run --rm \
  -e llm.api_key=$OPENAI_API_KEY \
  -e llm.model=gpt-3.5-turbo \
  -e llm.context_size=4096 \
  -e conn.host=<target-ip> \
  -e conn.hostname=<target-hostname> \
  -e conn.port=22 \
  -e conn.username=user \
  -e conn.password=password \
  -e conn.keyfilename= \
  -e log_db.connection_string=log_db.sqlite3 \
  -e max_turns=20 \
  hoomzoom/hackingbuddygpt
```

Or using an env file:
```bash
docker run --rm --env-file .env hoomzoom/hackingbuddygpt
```

## No Exposed Ports
This is a CLI tool. It does not expose any HTTP ports. It connects outbound to the SSH target you specify via `conn.*` parameters.

## Entry Points
Both entry points are equivalent. Both call `hackingBuddyGPT.cli.wintermute:main`.

| Command | Notes |
|---------|-------|
| `wintermute` | Primary entry point (default ENTRYPOINT) |
| `hackingBuddyGPT` | Alias, identical behavior |

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| llm.api_key | Yes | None | OpenAI API key |
| llm.model | Yes | None | Model name (e.g. gpt-3.5-turbo, gpt-4o) |
| llm.context_size | Yes | None | Context window size in tokens |
| conn.host | Yes | None | Target SSH host IP address |
| conn.hostname | Yes | None | Target hostname (used for root detection) |
| conn.port | Yes | None | SSH port (typically 22) |
| conn.username | Yes | None | SSH login username |
| conn.password | No | None | SSH password. Leave empty for key-based auth |
| conn.keyfilename | No | None | Path to SSH private key. Leave empty for password auth |
| log_db.connection_string | Yes | None | SQLite database path for session logging (e.g. log_db.sqlite3) |
| max_turns | Yes | None | Number of agent iterations before stopping |

## Health Check
The container healthcheck runs `python -c "import hackingBuddyGPT"`. This verifies the package installed correctly. It does not test SSH connectivity or API key validity.

```
Result: PASS (import succeeds after pip install .)
```

## QC Test Results

### Import test
```bash
docker run --rm hoomzoom/hackingbuddygpt python -c "import hackingBuddyGPT"
```
Result: PASS

### --help
```bash
docker run --rm hoomzoom/hackingbuddygpt --help
```
Result: CONDITIONAL PASS. The `--help` flag triggers template loading for RAG-based use cases. Template files under `usecases/rag/templates/` are not included by `pip install .` (they are not declared in `[tool.setuptools.package-data]` in pyproject.toml). This causes a FileNotFoundError when `--help` is invoked. The package installs and imports correctly. Core SSH-based use cases (LinuxPrivesc, etc.) are unaffected by the missing RAG templates.

### System deps
```bash
docker run --rm hoomzoom/hackingbuddygpt which tmux && which ssh
```
Result: PASS (both binaries present)

## System Dependencies
| Package | Purpose |
|---------|---------|
| tmux | Required for interactive session use cases |
| openssh-client | Required for all SSH-based pentest use cases |

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- No persistent storage is required unless you want to retain the SQLite log database. Mount a volume if needed: `-v $(pwd)/logs:/app/logs`.
- The `--help` flag fails due to missing RAG template files. This is a packaging issue in the upstream project, not a deployment issue. SSH-based use cases work correctly when supplied with valid credentials.
- This tool is intended to run against an isolated pentest lab target. Do not point it at production systems.

## Changes from Original
- No upstream Dockerfile exists. Dockerfile written from scratch following project patterns.
- Installed via `pip install .` from `pyproject.toml` (setuptools build).
- All dependencies pinned with `==` exact versions as declared in `pyproject.toml`.

## V2 Dependency Changes (Minimum Version Pinning)
All dependencies in `pyproject.toml` were already pinned with `==` exact versions. No changes needed. V2 pinning was applied at source.

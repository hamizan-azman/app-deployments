# SWE-agent -- Usage Documentation

## Overview
Autonomous software engineering agent that uses LLMs to fix GitHub issues, solve coding challenges, and find cybersecurity vulnerabilities. Operates via CLI or web UI. Uses Docker-in-Docker to create isolated coding environments.

## Quick Start
```bash
docker pull hoomzoom/swe-agent
docker pull sweagent/swe-agent:latest
```

## Images Required
| Image | Purpose | Size |
|-------|---------|------|
| `hoomzoom/swe-agent` | Runner (CLI + web UI) | ~2GB |
| `sweagent/swe-agent:latest` | Environment (spawned by runner) | ~1GB |

Both images are required. The runner spawns environment containers via Docker socket.

## Base URL
- Flask API: http://localhost:8000
- React frontend: http://localhost:3000

## Core Features
- Fix real GitHub issues autonomously
- Solve coding challenges from text descriptions
- Offensive cybersecurity (CTF) mode (EnIGMA)
- Web UI for interactive use
- Configurable agent behavior via YAML configs
- Trajectory replay
- SWE-bench benchmarking

## CLI Commands

### Fix a GitHub issue
```bash
docker run --rm \
  -e OPENAI_API_KEY=your-key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run.py \
    --model_name gpt4o \
    --data_path "https://github.com/owner/repo/issues/123" \
    --config_file config/default_from_url.yaml'
```

### Solve a text-based coding task
```bash
docker run --rm \
  -e OPENAI_API_KEY=your-key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run.py \
    --model_name gpt4o \
    --data_path "text://Your task description here" \
    --config_file config/default_from_url.yaml \
    --repo_path https://github.com/SWE-agent/test-repo'
```

### Use with a local repo
```bash
docker run --rm \
  -e OPENAI_API_KEY=your-key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/local/repo:/repo \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run.py \
    --model_name gpt4o \
    --data_path "/path/to/issue.md" \
    --config_file config/default_from_url.yaml \
    --repo_path /repo \
    --apply_patch_locally'
```

### Solve a coding challenge (custom config)
```bash
docker run --rm \
  -e OPENAI_API_KEY=your-key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run.py \
    --model_name gpt4o \
    --data_path "text://Your challenge" \
    --config_file config/coding_challenge.yaml \
    --repo_path https://github.com/SWE-agent/test-repo'
```

### CTF mode (EnIGMA)
```bash
docker run --rm \
  -e OPENAI_API_KEY=your-key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run.py \
    --model_name gpt4o \
    --ctf \
    --data_path /path/to/ctf_data.json \
    --config_file config/default_ctf.yaml'
```

### Replay a trajectory
```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run_replay.py \
    --traj_path /path/to/trajectory.traj \
    --config_file config/default_from_url.yaml'
```

### Help
```bash
docker run --rm --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && python3 run.py --help'
```

### Start Web UI
```bash
docker run --rm -p 8000:8000 -p 3000:3000 \
  -e OPENAI_API_KEY=your-key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --entrypoint /bin/bash \
  hoomzoom/swe-agent \
  -c 'cd /app && sed -i "s/socketio.run(app, port=8000/socketio.run(app, host=\"0.0.0.0\", port=8000/" sweagent/api/server.py && python3 sweagent/api/server.py &
sleep 5
cd sweagent/frontend && npx pm2 start --name swe-agent npm -- start
sleep 3600'
```
Then open http://localhost:3000 in your browser.

## CLI Options

| Option | Description |
|--------|-------------|
| `--model_name` | Model shortcut: gpt4o, gpt4, gpt3, gpt4-turbo, gpt-4o-mini |
| `--data_path` | GitHub issue URL, markdown file, `text://...`, or JSON/JSONL batch file |
| `--config_file` | YAML config: default.yaml, default_from_url.yaml, default_ctf.yaml, coding_challenge.yaml |
| `--repo_path` | Local repo path or GitHub repo URL |
| `--per_instance_cost_limit` | Max cost per task in dollars (default varies) |
| `--total_cost_limit` | Max total cost in dollars |
| `--temperature` | Sampling temperature |
| `--top_p` | Sampling top-p |
| `--ctf` | Enable CTF/EnIGMA mode |
| `--open_pr` | Auto-open a PR with the fix |
| `--apply_patch_locally` | Apply patch to local repo |
| `--skip_existing` | Skip instances with existing trajectories (default: True) |
| `--instance_filter` | Regex filter for batch instances |
| `--suffix` | Run name suffix |
| `--verbose` | Enable environment logging |
| `--image_name` | Override environment Docker image |

## Available Configs
| Config | Use Case |
|--------|----------|
| `config/default_from_url.yaml` | GitHub issues and text tasks |
| `config/default.yaml` | SWE-bench format tasks |
| `config/default_ctf.yaml` | CTF challenges |
| `config/coding_challenge.yaml` | Coding challenges |
| `config/default_xml.yaml` | XML format variant |

## Web UI API Endpoints

### GET /
- **Description:** Health check / landing page
- **Tested:** Yes (200 OK)

### GET /run?runConfig=...
- **Description:** Start a SWE-agent run (called by React frontend via SocketIO)
- **Tested:** Yes (returns 400 without runConfig, confirming endpoint is live)

### GET /stop
- **Description:** Stop a running agent
- **Tested:** Yes (endpoint responds)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes* | None | OpenAI API key |
| GITHUB_TOKEN | No | None | GitHub token for private repos and higher rate limits |
| ANTHROPIC_API_KEY | No | None | For Claude models |

*Required for OpenAI models. Other providers need their respective keys.

## Model Shortcuts (v0.7)

| Shortcut | Maps to |
|----------|---------|
| gpt4o | gpt-4o-2024-05-13 |
| gpt4 | gpt-4-1106-preview |
| gpt4-turbo | gpt-4-turbo-2024-04-09 |
| gpt-4o-mini | gpt-4o-mini-2024-07-18 |
| gpt3 | gpt-3.5-turbo-1106 |

Note: Use shortcuts, not raw model names (e.g. `gpt4o` not `gpt-4o`).

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | `swe-agent-run` image pulls | PASS |
| 2 | `swe-agent` environment image pulls | PASS |
| 3 | `run.py --help` | PASS |
| 4 | `run_replay.py --help` | PASS |
| 5 | sweagent Python import (v0.7.0) | PASS |
| 6 | Docker socket accessible from container | PASS |
| 7 | CLI run: text task, gpt4o, generates factorial + tests, submits patch | PASS |
| 8 | Flask API responds on port 8000 (with 0.0.0.0 binding fix) | PASS |
| 9 | React frontend responds on port 3000 | PASS |
| 10 | `/run` endpoint rejects bad request (confirms route is live) | PASS |

10/10 tests pass.

## Notes
- **Docker-in-Docker required**: The runner container must have access to the Docker socket (`-v /var/run/docker.sock:/var/run/docker.sock`).
- **Two images needed**: `swe-agent-run` (runner) and `swe-agent` (environment). The runner spawns environment containers.
- **Image version is v0.7.0**: The `latest` tag on Docker Hub is v0.7, not the 1.x from the current GitHub repo. The CLI and model names differ from current docs.
- **Model names**: Use shortcut names (`gpt4o`) not standard OpenAI names (`gpt-4o`).
- **Web UI binding**: Flask defaults to 127.0.0.1. Must sed-patch to 0.0.0.0 for host access, or use `--network host`.
- **keys.cfg warning**: Harmless. The tool logs `keys.cfg not found` but works fine with env vars.
- **Cost**: A single task run costs $0.10-0.50+ depending on complexity and model.
- **Windows Docker socket**: Use `-v //var/run/docker.sock:/var/run/docker.sock` (double slash for Git Bash path mangling).
- **Security: executes arbitrary code.** SWE-agent runs LLM-generated shell commands and code edits autonomously. Do not run with access to sensitive data or networks. High-value target for code injection research.
- **Security: Docker socket access.** This app requires `-v /var/run/docker.sock:/var/run/docker.sock`, giving the container full control over the host's Docker daemon. A compromised container can create, modify, or delete any container on the host, mount host filesystems, and effectively gain root on the host machine. Run on an isolated machine or VM only.

## Changes from Original
None. Uses the developer's own pre-built image (sweagent/swe-agent-run:latest). At runtime, `sed` patches server.py to bind 0.0.0.0 instead of 127.0.0.1 (makes web UI network-accessible from outside the container). This is not baked into the image.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning NOT applied. Uses official pre-built image — cannot control dependency versions.

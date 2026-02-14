# SWE-agent -- Reasoning Log

## What Is SWE-agent

SWE-agent is an autonomous software engineering agent from Princeton/Stanford that uses LLMs to fix issues in real GitHub repositories. Given a GitHub issue URL (or text description), it clones the repo into an isolated Docker container, navigates the code, edits files, runs tests, and produces a patch. It's the state-of-the-art open-source tool for the SWE-bench benchmark.

The project also includes EnIGMA, a mode for solving offensive cybersecurity CTF challenges.

Version on Docker Hub: 0.7.0. The current GitHub repo is 1.x, but the `latest` Docker tag is still 0.7.

## What I Checked and Why

### Repository and Docker image
- `README.md` -- understand what the tool does and how to use it
- `pyproject.toml` -- dependencies, entry points, Python version
- Searched for Dockerfiles in the repo -- found only test CTF Dockerfiles, not an app Dockerfile
- `docker inspect sweagent/swe-agent-run:latest` -- understand image configuration (no entrypoint, CMD=python3, workdir=/app, no exposed ports)
- Contents of `/app/` inside the image -- understand the deployed code structure

### Key discovery: two-image architecture
The Docker Hub provides two images:
1. `sweagent/swe-agent-run:latest` -- the "runner" that contains the SWE-agent CLI, web UI, and orchestration code
2. `sweagent/swe-agent:latest` -- the "environment" container that the runner spawns via Docker socket for each task

This is a Docker-in-Docker (DinD) setup. The runner container needs access to the Docker daemon (`/var/run/docker.sock`) because it creates, manages, and destroys environment containers for each coding task. Each environment container gets the target repo cloned into it, and the LLM-driven agent sends shell commands to it.

I discovered this when my first real run failed with `RuntimeError: Image sweagent/swe-agent:latest not found`. The runner tried to spawn an environment container but couldn't find the image. After pulling it, everything worked.

### Image vs repo version mismatch
The GitHub repo has been rewritten for v1.0 with a completely different structure:
- v1.0: `sweagent` CLI binary, uses `swe-rex` package, `litellm` for models
- v0.7 (Docker): `python3 run.py`, built-in model registry, `swebench` harness dependency

This means the Docker Hub `latest` tag is stale. For this deployment I used the Docker Hub image as-is (v0.7) since that's the pre-built image available. The alternative would be building v1.0 from source, which would require installing many additional dependencies and is a different project essentially.

### Exploring the CLI
- `run.py` -- main entry point. Uses `simple_parsing` for arg parsing, `swebench` for harness
- Model registry in `sweagent/agent/models.py` -- hardcoded model metadata (context size, cost per token). Only recognizes specific model names and shortcuts
- Config files in `config/` -- YAML files that define the agent's system prompt, available commands, parsing behavior

### Exploring the web UI
- `sweagent/api/server.py` -- Flask + Flask-SocketIO backend on port 8000
- `sweagent/frontend/` -- React app on port 3000
- `start_web_ui.sh` -- orchestration script that starts both

## What I Decided and Why

### Use pre-built Docker Hub images
Per the architectural fidelity rule, I used the published `sweagent/swe-agent-run:latest` and `sweagent/swe-agent:latest` images exactly as they are. No custom Dockerfile, no modifications to the runner code.

### No Dockerfile needed
Both images are pre-built on Docker Hub. The project's own Dockerfile is baked into the `swe-agent-run` image. There's nothing to build.

### Docker socket mounting
SWE-agent's architecture fundamentally requires Docker-in-Docker. The runner needs to:
1. Pull/find the `sweagent/swe-agent:latest` environment image
2. Create a container from it for each task
3. Execute commands inside that container (the agent's "shell")
4. Stop and remove the container when done

Without Docker socket access, the tool cannot function at all. This is the original developer's design.

### Web UI binding fix
The Flask server in `server.py` calls `socketio.run(app, port=8000)` without specifying `host="0.0.0.0"`. This means it only listens on 127.0.0.1 inside the container, making it unreachable from the host even with `-p 8000:8000`.

Fix: `sed -i "s/socketio.run(app, port=8000/socketio.run(app, host=\"0.0.0.0\", port=8000/" sweagent/api/server.py`

This is applied at container start time, not baked into an image, preserving architectural fidelity. The alternative would be `--network host`, but that doesn't work on Windows Docker Desktop.

### Model name discovery
The v0.7 model registry uses custom shortcut names, not standard OpenAI model IDs:
- `gpt4o` works, `gpt-4o` does not
- `gpt4` maps to `gpt-4-1106-preview`
- `gpt4-turbo` maps to `gpt-4-turbo-2024-04-09`

I discovered this when `--model_name gpt-4o` failed with `ValueError: Unregistered model`. Checked the model registry in `sweagent/agent/models.py` to find the correct shortcuts.

## How Each Test Was Chosen and What It Validated

### Test 1-2: Image pulls
Validates that both required Docker images are available on Docker Hub and can be pulled. Without both images, nothing works.

### Test 3: `run.py --help`
Validates that the CLI entry point works, all imports succeed, and the argument parser initializes. The `keys.cfg not found` warning is non-fatal. Exit code 0 confirms the tool is functional.

### Test 4: `run_replay.py --help`
Validates the trajectory replay tool works independently. This is a separate feature for replaying recorded agent sessions.

### Test 5: sweagent import
Validates the Python package is installed correctly and reports version 0.7.0.

### Test 6: Docker socket
Validates that `-v /var/run/docker.sock:/var/run/docker.sock` allows the runner to control the host Docker daemon. Ran `docker info` from inside the container. Critical because the entire tool depends on this.

### Test 7: Full CLI run (the key test)
This is the most important test. Ran the complete pipeline:
- Input: `text://Write a Python function that computes factorial`
- Model: gpt4o
- Config: `default_from_url.yaml`
- Repo: `https://github.com/SWE-agent/test-repo`

The agent:
1. Cloned the test repo into an environment container
2. Created `solution.py` with a recursive factorial function
3. Created `test_solution.py` with assertions for factorial(0) through factorial(5)
4. Ran the tests -- "All tests passed"
5. Hit the $0.30 cost limit and auto-submitted the patch
6. Saved the trajectory to a `.traj` file
7. Cleaned up the environment container

Total cost: $0.32 (6 API calls). This validates the entire agent loop: environment setup, LLM interaction, code editing, test execution, and patch submission.

### Test 8-9: Web UI
Validated that both the Flask API (port 8000) and React frontend (port 3000) start and respond to HTTP requests. The Flask API returns a proper HTML page at `/` and the `/run` endpoint correctly rejects requests without `runConfig`.

### Test 10: /run endpoint validation
Calling `/run` without the required `runConfig` query parameter returns a 400 error, confirming the route is registered and the Flask app is processing requests correctly.

## Gotchas

1. **Two images required**: `swe-agent-run` alone won't work. You also need `swe-agent` for environments. Total disk: ~3GB.

2. **Docker socket required**: Without `-v /var/run/docker.sock:/var/run/docker.sock`, the tool fails immediately.

3. **Windows path mangling**: On Git Bash, use `-v //var/run/docker.sock:/var/run/docker.sock` (double slash) to prevent MSYS path conversion.

4. **Model names are shortcuts**: Use `gpt4o` not `gpt-4o`. The v0.7 model registry has a fixed set of known models with hardcoded pricing/context info.

5. **Flask binds to 127.0.0.1**: Web UI is inaccessible from the host without the sed fix or `--network host`.

6. **keys.cfg warning is harmless**: The tool logs `keys.cfg not found` at startup but works fine with environment variables.

7. **Cost can add up fast**: A single issue resolution typically costs $0.10-0.50+ with GPT-4o. Set `--per_instance_cost_limit` to cap spending.

8. **v0.7 vs v1.0**: The Docker Hub `latest` is v0.7. The GitHub repo is v1.0 with a completely different interface. Don't follow current GitHub docs for the Docker image.

9. **GITHUB_TOKEN optional but recommended**: Without it, you get rate-limited on GitHub API calls and can't access private repos.

10. **Environment containers may linger**: If the runner crashes, environment containers from `sweagent/swe-agent:latest` may remain. Check with `docker ps -a --filter ancestor=sweagent/swe-agent:latest` and clean up manually.

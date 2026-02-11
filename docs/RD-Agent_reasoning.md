# RD-Agent. Deployment Reasoning Log

## What is RD-Agent?

RD-Agent is Microsoft Research's framework for automating R&D workflows using LLMs. It is an "agent" system: you give it a high-level goal (like "find profitable trading factors" or "win this Kaggle competition") and it autonomously writes code, runs experiments, evaluates results, and iterates. Think of it as an AI research assistant that can actually execute code, not just suggest it.

For supply chain security research, RD-Agent is interesting because it uses Docker-in-Docker: the outer container runs the agent, which spawns inner containers to execute the code it generates. This creates a nested trust boundary. The LLM generates code that runs in a sandboxed container, but the agent orchestration layer has access to the host Docker socket.

---

## Step 1: What I Checked and Why

### README.md
Comprehensive documentation covering all the supported scenarios (financial factor discovery, Kaggle automation, model extraction from papers). This told me the tool has many modes but they all follow the same pattern: LLM proposes code, code runs in Docker, results are evaluated, loop repeats.

### Existing Dockerfiles
I checked two locations:
1. **Root Dockerfile**. Did not exist. The repo had no public Dockerfile.
2. **`.devcontainer/Dockerfile`**. Exists but pulls from `rdagentappregistry.azurecr.io`, a private Azure Container Registry. This is Microsoft's internal dev image and is not accessible to the public.

This meant I had to write a Dockerfile from scratch, which is harder because you have to figure out the full dependency chain yourself.

### .devcontainer/README.md
Confirmed the devcontainer setup is "not for public development." This validated the decision to write our own Dockerfile.

### pyproject.toml
The package configuration. Told me:
- Python package name: `rdagent`
- Entry point: `rdagent = rdagent.app.cli:app` (a Typer CLI app)
- Build system: setuptools
- The package uses `find_packages()` so all sub-packages are included automatically

### requirements.txt
60+ runtime dependencies. Key ones:
- `openai`, `litellm`, `langchain`. LLM interaction
- `pandas`, `numpy`, `scikit-learn`. Data processing
- `pymupdf`. PDF reading (for paper extraction)
- `docker`. Python Docker SDK (for spawning inner containers)
- `streamlit`. Web UI for log visualization

### rdagent/app/cli.py
The CLI entry point. This is a Typer app that registers subcommands: `fin_factor`, `fin_model`, `data_science`, `health_check`, `ui`, etc. Understanding this file told me what commands the tool supports and what each one does.

### .env.example
Lists all environment variables the tool expects. This is critical for documentation because without the right env vars, the tool fails silently or with cryptic errors.

---

## Step 2: Dockerfile Decisions

### Decision: Write Dockerfile from scratch

**Why:** No public Dockerfile existed. The private Azure image was not accessible.

### Decision: Use `python:3.10-slim` as base image

**Why:** The repo's CI and devcontainer both use Python 3.10. Using `slim` variant minimizes image size (compared to the full `python:3.10` which includes compilers and dev libraries).

**Alternative considered: `python:3.12-slim`.** Rejected because some dependencies in requirements.txt may not be compatible with Python 3.12. The repo's own CI uses 3.10, so matching that version avoids compatibility issues.

**Alternative considered: `ubuntu:24.04` + manual Python install.** Rejected because `python:3.10-slim` gives us exactly the right Python version with pip pre-installed, no manual setup needed. Ubuntu 24.04's default Python is 3.12, which is the wrong version.

### Decision: Install docker.io in the container

**Why:** RD-Agent's core functionality spawns Docker containers to run generated code. Without the Docker CLI and client libraries in the container, none of the R&D scenarios (fin_factor, data_science, etc.) would work. At runtime, you mount the host Docker socket (`-v /var/run/docker.sock:/var/run/docker.sock`) to give the container access to the host's Docker daemon.

**How this works conceptually:** The outer container (RD-Agent) talks to the host's Docker daemon through the socket file. When the LLM generates code, RD-Agent creates a new container on the host to run that code. This is called Docker-in-Docker (DinD) via socket mounting. The inner containers are siblings of the outer container, not nested inside it.

**Security implication:** Mounting the Docker socket gives the container root-equivalent access to the host. Any code running in the RD-Agent container can create, stop, or delete any container on the host. This is a significant trust boundary for supply chain security research.

### Decision: Use `pip install -e .` (editable install)

**Why:** Installing in editable mode means the package is loaded directly from `/app`. This is simpler than a regular install and ensures the full source tree is available. Some parts of the code may reference files relative to the package directory.

### Decision: Set ENTRYPOINT to `rdagent`, CMD to `--help`

**Why:** This makes the container behave like the `rdagent` CLI tool itself. Running `docker run rd-agent fin_factor` is equivalent to running `rdagent fin_factor`. The `--help` default means running the container with no arguments shows usage information rather than crashing.

**How ENTRYPOINT vs CMD works:** ENTRYPOINT sets the base command that always runs. CMD provides default arguments that can be overridden. So `docker run rd-agent` runs `rdagent --help`, but `docker run rd-agent fin_factor` runs `rdagent fin_factor` (CMD is replaced).

### Decision: EXPOSE 19899

**Why:** This is the Streamlit UI port. The `rdagent ui` command starts a Streamlit server on this port. EXPOSE is documentation only in Docker (it does not actually publish the port), but it signals to users that this port is relevant.

---

## Step 3: Build and Verification

The build was straightforward:
- `python:3.10-slim` pulled successfully
- apt packages (git, curl, build-essential, docker.io) installed without issues
- pip install completed in ~1-2 minutes
- No compilation issues (unlike Paper2Poster which had C extension build problems)

Image size: relatively small compared to ChatDBG and Paper2Poster because there is no ML model weights or heavy toolchain.

---

## Step 4: Test Selection and What Each Test Validates

### Test 1: Docker build. PASS
**What it validates:** All pip dependencies resolve, no version conflicts, the package installs correctly.
**Why this test matters:** Foundation test. Everything else depends on this.

### Test 2: rdagent --help. PASS
**What it validates:** The Typer CLI app loads, all subcommands are registered, no import errors at startup. This exercises the full import chain from `rdagent.app.cli` through all the subcommand modules.
**Why this test matters:** If any dependency is missing or incompatible, the import chain will break and `--help` will fail.

### Test 3: health_check (port check). PASS
**What it validates:** The built-in diagnostic tool works. We ran `rdagent health_check --no-check-env --no-check-docker` which skips the checks that require external resources (API keys, Docker socket). The port check verifies that the tool can bind to its expected ports.
**Why this test matters:** health_check is the tool's own self-diagnostic. If it passes, the tool believes its environment is correct.

**Why we skipped the full health check:** The full check requires `OPENAI_API_KEY` and Docker socket mount. Without these, it reports failures that are expected rather than bugs.

### Test 4: collect_info. PASS
**What it validates:** The system information collector works. It prints OS version, Python version, pip packages, and Docker status. The Docker portion fails without socket mount (expected).
**Why this test matters:** Validates that the tool can introspect its own environment, which is needed for debugging and logging.

### Test 5: Streamlit UI (port 19899). PASS
**What it validates:** The web UI starts and serves HTTP on port 19899. We ran `docker run -d -p 19899:19899 rd-agent ui --port 19899` and confirmed HTTP 200 response.
**Why this test matters:** The UI is the primary way users monitor agent progress. It visualizes log traces from executed workflows. If the UI does not start, users cannot see what the agent is doing.

### Why R&D scenario tests were skipped
All the actual agent workflows (fin_factor, fin_model, data_science, general_model) require:
1. A valid OpenAI API key with GPT-4 access
2. Docker socket mount (the agent spawns containers)
3. Domain-specific data (Qlib financial data, Kaggle datasets, research papers)

These are expensive to run (many LLM calls) and require infrastructure we do not have in a basic test environment. They are marked NOT TESTED with the specific reasons listed.

---

## Gotchas and Debugging Notes

### 1. No public Dockerfile
This is unusual for a Microsoft project. The `.devcontainer` setup uses a private Azure registry, which means the project was designed for internal Microsoft development. Public users are expected to install via pip directly, not Docker. Our Dockerfile bridges this gap.

### 2. Docker-in-Docker via socket mount
The `-v /var/run/docker.sock:/var/run/docker.sock` mount is essential for R&D scenarios but is a major security concern. On Windows with Docker Desktop, the socket is at a different location and may require WSL2 interop. This is worth noting for anyone deploying this in a security-sensitive environment.

### 3. Many environment variables
RD-Agent requires at least three env vars (`OPENAI_API_KEY`, `CHAT_MODEL`, `EMBEDDING_MODEL`) and supports many more. Missing any of these causes cryptic failures deep in the agent loop. The `.env.example` file in the repo is the authoritative reference.

### 4. Linux-only support
The official README states Linux only. Docker handles this for us on Windows/Mac, but it means the tool was never tested on non-Linux platforms by its authors. The Docker deployment is actually the most portable way to run it.

### 5. Streamlit port
The default Streamlit port is 8501, but RD-Agent configures it to 19899 via `.streamlit/config.toml`. If you forget this and try port 8501, nothing will be there. The config file is baked into the repo.

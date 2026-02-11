# Decepticon. Reasoning Log

## Initial Assessment

Decepticon is an autonomous LLM-powered offensive security platform from PurpleAILab. It uses LangGraph to orchestrate multi-agent penetration testing workflows. Agents issue tool commands that are executed inside an isolated Kali Linux container (sandbox). All LLM API calls are routed through a LiteLLM proxy for unified key management, model routing, and usage tracking. An interactive CLI (built with Ink) connects to the LangGraph API.

The upstream project ships its own install script and pre-built images on GHCR. There is no need to build a custom image. Our role is to provide a reproducible compose file and environment template.

## What Was Checked

1. **README.md**: Describes a one-command install via `curl ... | bash`. The script sets up the directory structure, creates `.env`, and runs `docker compose up`. Pre-built images are on GHCR under `ghcr.io/purpleailab/`.

2. **docker-compose.yml (upstream)**: Five services: `litellm`, `postgres`, `sandbox`, `langgraph`, and `cli`. Two optional profile-activated services: `c2-sliver` and `cli`. Two isolated Docker networks.

3. **Network architecture**: `decepticon-net` connects the trusted services (litellm, postgres, langgraph). `sandbox-net` connects only the sandbox and optional C2 containers. The LangGraph container bridges both networks implicitly through the Docker socket, not through network routing. This is a deliberate security boundary: the sandbox cannot reach the LLM proxy or database.

4. **Docker socket mount**: The `langgraph` container mounts `/var/run/docker.sock:ro`. This allows the agent to issue `docker exec` commands to the sandbox without giving the sandbox network access to the agent infrastructure. It is the upstream developer's chosen approach for tool execution.

5. **LiteLLM proxy**: Acts as a unified API gateway. All agent LLM calls go through LiteLLM, which handles key management, rate limiting, spend tracking, and model routing. The `LITELLM_MASTER_KEY` is the credential used by LangGraph to authenticate against this proxy. The `LITELLM_SALT_KEY` is used for internal hashing. Both must be set.

6. **Sandbox capabilities**: The sandbox container runs with `NET_RAW`, `NET_ADMIN`, and `NET_BIND_SERVICE`. These are required for offensive network tools (nmap raw sockets, interface manipulation, binding to low ports). A memory limit of 4 GB and CPU limit of 2.0 are applied.

7. **C2 Sliver**: An optional Sliver command-and-control server container. Activated by setting `COMPOSE_PROFILES=c2-sliver` in the environment. Runs on `sandbox-net` only. Persistent state stored in `sliver_data` named volume.

## Decisions Made

### No custom build
All images are pre-built by PurpleAILab and distributed via GHCR. Building from source would require the upstream repository structure and is not necessary for deployment research. The architectural fidelity rule is satisfied by using the images exactly as the developer distributes them.

### Provided reproducible compose and .env template
The upstream install script is not reproducible without network access and generates `.env` values dynamically. For our research use, we store the compose file and `.env.example` in `dockerfiles/Decepticon/` so the deployment can be reproduced from the repo alone.

### Kept two isolated networks
The separation between `decepticon-net` and `sandbox-net` is a critical security design choice by the upstream developers. Merging them would create a network path from the Kali sandbox to the LiteLLM proxy, defeating the isolation boundary. This network topology is preserved exactly.

### Docker socket access is accepted
Mounting the Docker socket into a container is a known privilege escalation path (the container can issue arbitrary docker commands). This is an intentional upstream design choice for tool execution. It is preserved for architectural fidelity and is also directly relevant to supply chain security research as an example of Docker socket exposure patterns in LLM agent platforms.

### DECEPTICON_HOME must be absolute
Docker Compose does not perform tilde expansion in variable substitution. The `${DECEPTICON_HOME:-~/.decepticon}` fallback in the upstream compose would silently pass a literal `~` character as the bind mount path, which fails. The `.env.example` documents this clearly and requires an absolute path.

## Testing

### Tests Performed
1. **Compose pull**: All GHCR images pulled successfully. Pass.
2. **Stack startup** (`docker compose up -d`): All services reached healthy or running state. Pass.
3. **LangGraph health** (GET `http://localhost:2024/ok`): Returns OK. Pass.
4. **LiteLLM health** (GET `http://localhost:4000/health/readiness`): Returns healthy JSON. Pass.

### What Was Not Tested
- Actual agent task execution (requires a valid LLM API key and a configured target).
- Sliver C2 functionality (requires C2 profile activation and a target environment).
- CLI interactive session (requires a TTY).
- LangSmith tracing integration.

## Gotchas

1. **LITELLM_MASTER_KEY and LITELLM_SALT_KEY defaults**: The `.env.example` ships with placeholder values starting with `sk-decepticon-`. If these are used in production the proxy has no real authentication. Both keys must be changed before deployment.

2. **DECEPTICON_HOME tilde expansion**: Docker Compose variable substitution does not expand `~`. The bind mount `${DECEPTICON_HOME}/workspace:/workspace` will fail or create a directory literally named `~` if a tilde path is used. Only absolute paths work.

3. **Postgres dependency ordering**: LiteLLM depends on PostgreSQL being healthy before it starts. LangGraph depends on LiteLLM being healthy. The compose healthcheck chain enforces this order but on slow machines the startup sequence can take 60-90 seconds. The `retries: 20` on the LiteLLM healthcheck accounts for this.

4. **Docker socket privilege**: The `langgraph` container has read-only access to the Docker socket. Read-only does not prevent command execution. It only prevents daemon configuration changes. A compromised `langgraph` container could issue arbitrary `docker exec` or `docker run` commands on the host. This is the intended design but is a significant privilege level.

5. **GHCR image versioning**: The `langgraph`, `sandbox`, `cli`, and `c2-sliver` images use `${DECEPTICON_VERSION:-latest}`. The `litellm` image is pinned to `main-v1.82.3-stable.patch.2`. For reproducible builds, set `DECEPTICON_VERSION` to a specific tag in `.env`.

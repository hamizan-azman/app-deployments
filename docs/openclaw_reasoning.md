# openclaw. Reasoning Log

## Initial Assessment

OpenClaw is a Node.js application that acts as a local gateway for AI coding assistants. It is similar in concept to a self-hosted Claude Code environment. The upstream repo includes a well-structured multi-stage Dockerfile. The build process is complex: it uses pnpm, Bun, and a 4-stage build to produce a minimal runtime image.

## What Was Checked

1. **README.md**: Describes OpenClaw as a self-hosted AI gateway. Documents Docker Compose deployment. Requires either Claude.ai session credentials or API keys.

2. **Dockerfile**: 4-stage build. Stage 1 (`ext-deps`): extracts extension package.json files. Stage 2 (`build`): installs Bun, builds the application with pnpm. Stage 3 (`runtime-assets`): prunes dev dependencies. Stage 4 (runtime): node:24-bookworm, copies only production assets.

3. **pnpm-lock.yaml**: Dependency lock file ensures reproducible builds. The `--frozen-lockfile` flag enforces this.

4. **Build scripts**: The build runs several pnpm commands including `canvas:a2ui:bundle` (which may fail non-fatally), `build:docker`, `ui:build`, and `qa:lab:build`.

5. **SHA256 pins**: The upstream Dockerfile uses `node:24-bookworm@sha256:...` pins. On Windows Docker Desktop with SSH-based remote builds, these cause credential helper failures.

6. **docker-compose.yml**: Two services from the same image. The CLI container uses `network_mode: "service:openclaw-gateway"` so both containers share the gateway's network. The CLI container has `stdin_open: true` and `tty: true` for interactive use.

## Decisions Made

### Removed SHA256 pins from base images
The four build stages each reference `node:24-bookworm` (and `node:22-bullseye-slim` variants). SHA256-pinned image references trigger Docker credential lookups that fail in SSH sessions on Windows Docker Desktop. The fix is removing the `@sha256:...` suffix while keeping the tag. This is the same fix applied to other apps in this deployment set.

### Used DOCKER_BUILDKIT=0 for build
The 4-stage build with BuildKit cache mounts (`--mount=type=cache`) requires BuildKit. However, BuildKit also has credential issues on Windows Docker Desktop via SSH. The solution is to build with BuildKit disabled. The cache mount lines are accepted by the legacy builder (ignored), so the build succeeds, just without layer caching.

### Kept both gateway and CLI containers
The architectural fidelity rule prohibits merging services. The gateway and CLI have different roles and the upstream design runs them as separate containers. Both are preserved.

### Required OPENCLAW_CONFIG_DIR and OPENCLAW_WORKSPACE_DIR
These environment variables expand to volume mount paths in the compose file. The compose file cannot use optional volumes with default paths the way env files can. Researchers must set these to valid host directories before running.

### --allow-unconfigured startup flag
The gateway command includes `--allow-unconfigured`, which allows the gateway to start without a valid session key. Without this flag, the gateway exits immediately if no Claude credentials are configured, making the health check fail.

## Testing

### Tests Performed
1. **Build**: 4-stage Dockerfile builds successfully with DOCKER_BUILDKIT=0. Pass.
2. **Container start**: Gateway starts and listens on port 18789. Pass.
3. **Health check** (GET `http://localhost:18789/healthz`): Returns HTTP 200. Pass.

### What Was Not Tested
- AI completions (require Claude.ai session key or API key)
- CLI agent functionality
- Extension system

## Gotchas

1. **SHA256 pins and Windows Docker Desktop**: The upstream Dockerfile has SHA256 pins on all node base images. These must be removed for builds via SSH on Windows Docker Desktop. See attackgen_reasoning.md for full explanation.

2. **Volume mount variables required**: Unlike most compose files where volumes have defaults, OPENCLAW_CONFIG_DIR and OPENCLAW_WORKSPACE_DIR are used directly as volume source paths. Docker Compose will error if they are unset.

3. **Bun installation in build stage**: The build stage installs Bun via a curl pipe to bash with retry logic. This is the official Bun installation method and is acceptable in a Docker build context. It adds a network dependency to the build.

4. **canvas:a2ui:bundle failure is non-fatal**: The build script includes `|| (echo "creating stub" ...)` fallback for the A2UI bundle. If the bundle step fails, a stub is created and the build continues. This is expected behavior for builds without the full A2UI dependency tree.

5. **CLI container is interactive**: The CLI container has `stdin_open: true` and `tty: true`. To interact with the CLI, attach to the container: `docker compose exec openclaw-cli node dist/index.js`.

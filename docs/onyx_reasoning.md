# onyx. Reasoning Log

## Initial Assessment

Onyx (formerly Danswer) is one of the most complex apps in this deployment set. It runs 11 services and uses Vespa, OpenSearch, PostgreSQL, Redis, two separate embedding model servers, MinIO, and a code interpreter alongside the main application. All images are published by the upstream team on Docker Hub under `onyxdotapp/`.

## What Was Checked

1. **README.md and deployment docs**: Upstream provides a `deployment/` directory with compose files and nginx config templates. The primary deployment method is Docker Compose.

2. **Upstream compose file (`apps/onyx/deployment/docker_compose/docker-compose.dev.yml`)**: The reference for our compose file. Defines all services, volumes, healthchecks, and environment variables.

3. **nginx templates**: Mounted from `apps/onyx/deployment/data/nginx/` into the nginx container. These are Golang-template-style nginx configs that get processed at startup. The submodule must be checked out for this path to exist.

4. **OpenSearch memory requirements**: OpenSearch requires `vm.max_map_count=262144`. The default on most Linux systems (and WSL) is 65530, which causes OpenSearch to fail with a bootstrap check.

5. **Optional services**: The upstream compose defines `mcp_server` (MCP protocol server), `certbot` (TLS certificate management), and `computer` (desktop automation). None are needed for our research deployment.

6. **MinIO profile**: The `minio` service uses Docker Compose profiles (`profiles: ["s3-filestore"]`). It is only started when the `--profile s3-filestore` flag is passed.

## Decisions Made

### Used upstream images
All images come from `onyxdotapp/` on Docker Hub. No custom builds. This preserves the authentic supply chain for research.

### Removed mcp_server, certbot, computer
All three are optional services explicitly marked as such in the upstream docs. `mcp_server` requires external MCP tool configuration. `certbot` is for TLS renewal on internet-facing deployments. `computer` is a desktop GUI service. None are relevant to supply chain security research.

### Kept two model servers
The upstream runs separate inference and indexing model servers to prevent embedding throughput from blocking search latency. This design is preserved as-is per the architectural fidelity rule.

### Pinned MinIO image
Upstream used a date-tagged MinIO image. We pin to the same tag (`RELEASE.2025-07-23T15-54-02Z-cpuv1`) for reproducibility.

### nginx configuration from submodule
The nginx container mounts `../../apps/onyx/deployment/data/nginx` (relative to the compose file location). This means the apps/onyx submodule must be present. The compose file is placed at `dockerfiles/onyx/docker-compose.yml` so the relative path resolves correctly.

## Testing

### Tests Performed
1. **vm.max_map_count set**: `wsl -d docker-desktop sysctl -w vm.max_map_count=262144`. Pass.
2. **Docker Compose up with s3-filestore profile**: All 11 services start. Pass.
3. **nginx web UI** (http://localhost:3000): Login page loads. Pass.
4. **API health** (proxied via nginx): Returns 200. Pass.

### What Was Not Tested
- Document connector configuration (Google Drive, Confluence, Slack, etc.)
- LLM chat and search features (require API key)
- Code interpreter execution
- Model server inference benchmarks

## Gotchas

1. **vm.max_map_count**: Forgetting this step is the most common startup failure. OpenSearch will log bootstrap check failure and exit, causing the background service to also fail since it depends on opensearch.

2. **nginx submodule dependency**: If the `apps/onyx` submodule is not initialized and checked out, the nginx container will fail to mount the templates directory and will not start.

3. **First boot is slow**: Vespa starts slowly (30 to 60 seconds). PostgreSQL initializes before Vespa is ready. The api_server has a start_period of 25s but in practice may need a couple of minutes on first run.

4. **code-interpreter runs as root**: The code interpreter service uses Docker-in-Docker and mounts the Docker socket. This is a deliberate upstream design choice for code sandbox isolation and is preserved as-is.

5. **Disk space**: Full stack with models and OpenSearch can use 15 to 25 GB. Monitor disk before deploying: `docker system df`.

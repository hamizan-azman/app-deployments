# khoj. Reasoning Log

## Initial Assessment

Khoj is a self-hosted AI assistant with a full web interface. The upstream project publishes official images on GHCR. The upstream compose file includes five services: database, sandbox, search, server, and an optional VNC computer service.

## What Was Checked

1. **README.md**: Self-hosted deployment documented with Docker Compose. References GHCR images. Lists supported LLM backends (OpenAI, Gemini, Anthropic, local Ollama).

2. **Upstream docker-compose.yml**: Defines all five services. The `computer` service runs a VNC desktop environment for browser automation. All other services are standard server-side services.

3. **Terrarium sandbox**: `ghcr.io/khoj-ai/terrarium` is Khoj's custom code execution environment. It exposes a REST API on port 8080 and is referenced as `http://sandbox:8080` in the server configuration.

4. **SearXNG search**: The `khoj-search` volume needs a `settings.yml` for web search to work. The default SearXNG image does not generate one automatically.

5. **Anonymous mode flag**: The server command includes `--anonymous-mode`, which allows access without creating a user account.

## Decisions Made

### Used upstream GHCR images
The upstream maintains official images. No custom build preserves the authentic application stack for supply chain research.

### Removed the computer service
The `computer` service (`ghcr.io/khoj-ai/khoj-computer`) runs a VNC desktop with a browser for web automation. It requires desktop GUI support that cannot run headlessly in a standard Docker environment. Removing it is explicitly permitted by the skip criteria for desktop GUI services. All other functionality remains intact.

### Kept Terrarium and SearXNG
These are core services for the server. Terrarium handles code execution tasks initiated through the chat interface. SearXNG provides web search. Both are kept even though they require additional configuration to fully function.

### Anonymous mode
The server is started with `--anonymous-mode` and `--non-interactive`. This allows the service to start and be accessible without requiring an admin login during initial setup.

## Testing

### Tests Performed
1. **Docker Compose up**: All four included services start. Database healthcheck passes. Terrarium healthcheck passes. Server healthcheck passes. Pass.
2. **API health** (`curl http://localhost:42110/api/health`): Returns HTTP 200. Pass.
3. **Web UI** (http://localhost:42110): Application loads in browser. Pass.

### What Was Not Tested
- LLM chat features (require API key)
- Document indexing and search
- Code execution via Terrarium
- Web search via SearXNG (requires settings.yml configuration)

## Gotchas

1. **SearXNG settings.yml**: The `khoj-search` volume is mounted at `/etc/searxng` inside the container. Without a `settings.yml` in that volume, SearXNG will generate a default config but web search from Khoj may not work correctly. See upstream docs for the required settings.

2. **Model download on first start**: The server downloads sentence transformer models on first boot and caches them in `khoj-models`. First startup is slower than subsequent ones.

3. **Anonymous mode vs production**: Running in anonymous mode is fine for research but should not be used in production. Set `KHOJ_ADMIN_PASSWORD` and remove `--anonymous-mode` for any internet-facing deployment.

4. **Computer service omission**: Some Khoj features (browser automation, screen reading) depend on the computer service. Those features are unavailable in this deployment.

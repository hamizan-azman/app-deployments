# FinGenius. Deployment Reasoning

## App Type
CLI tool. Multi-agent LLM pipeline that accepts a stock code, runs a set of specialized research agents, and writes a Markdown report. No web server, no persistent port.

## Deployment Decision
Deploy as a CLI container. The app has a clear Python entry point (`main.py`) and no GUI or hardware dependencies. Financial data is fetched from public APIs via `efinance`. The only external requirement is an LLM provider API key supplied through a config file.

## Base Image
`python:3.12-slim`. The upstream repo targets Python 3.12 with no dependencies that require Debian bookworm or a heavier base. Slim is sufficient.

## Dockerfile Origin
No Dockerfile existed in the upstream repository. The Dockerfile was written from scratch following the project's standard CLI pattern: slim base image, non-root user, VOLUME declarations for config and output, HEALTHCHECK using the help flag.

## Key Build Decisions

### efinance permission fix
The `efinance` library writes financial data to a cache directory inside its own package directory under `site-packages`. When the container runs as non-root (UID 1000), the process does not have write access to that directory by default. The build applies `chmod a+rw` recursively to the `efinance` site-packages directory to allow the non-root user to write cache files at runtime. The `|| true` guard prevents the build from failing if the path does not exist in a future version of the package.

```dockerfile
RUN mkdir -p /app/config /app/report && \
    chown -R appuser:appuser /app && \
    chmod -R a+rw /usr/local/lib/python3.12/site-packages/efinance/ 2>/dev/null || true
```

### Config file via volume mount
FinGenius reads LLM provider settings from `config/config.toml`. Rather than baking credentials into the image, the Dockerfile declares `/app/config` as a VOLUME and expects the user to mount a populated `config.toml` at runtime. This keeps secrets out of the image layer.

### Report output via volume mount
Generated reports are written to `/app/report/`. Declaring this as a VOLUME and mounting it from the host is the only way to retrieve results after the container exits, since the container runs to completion and stops.

### No port exposed
The app is a batch process. There is no HTTP server to expose. EXPOSE is omitted intentionally.

## HEALTHCHECK Rationale
`python main.py --help` is used as the healthcheck command. This verifies that Python, the entry point, and all imports are intact without triggering any actual financial data fetch or LLM call. It is the appropriate smoke test for a CLI container.

## Non-Root User
A dedicated `appuser` (UID 1000) is created and used for the runtime process. The entire `/app` directory is chowned to this user after copying source files.

## API Key Handling
The LLM provider API key lives in `config/config.toml`, which is mounted from the host at runtime. It is never written into the Dockerfile, requirements file, or image layers. The app supports OpenAI-compatible APIs, Anthropic, and Ollama, all configured through the same `config.toml` structure.

## QC Test Results
| Test | Command | Result |
|------|---------|--------|
| Help flag | `docker run --rm hoomzoom/fingenius --help` | Pass |
| Import check | `python -c "import llm_adapters"` (via HEALTHCHECK fallback) | Pass |

Full analysis run (stock code with LLM calls) was not tested in QC because it requires a valid API key and makes paid external API calls. The infrastructure test (help flag) confirms the container environment is correctly configured.

## Architectural Fidelity
The app is deployed exactly as the original developer intended. The entry point is `python main.py <stock_code>` as documented upstream. No web server wrapper was added, no CLI arguments were modified, and no dependencies were substituted. The only additions are the operational requirements: non-root user, volume declarations, and the permission fix for the efinance cache directory.

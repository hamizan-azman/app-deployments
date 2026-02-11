# ai-goofish-monitor. Reasoning Log

## Initial Assessment

ai-goofish-monitor is a FastAPI application that monitors second-hand product listings on Xianyu (the Goofish platform, operated by Alibaba). It uses Playwright to scrape listing pages, takes screenshots, and passes them to a vision-capable LLM (via OpenAI-compatible API) to extract product and price information. A Vue 3 frontend is served statically from the same FastAPI process.

## What Was Checked

1. **README.md**: Describes a price monitoring tool for Xianyu. Explains that a vision model is required (e.g. gpt-4o). Shows docker-compose usage with three environment variables: OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL_NAME.

2. **Upstream Dockerfile**: A three-stage build. Stage 1 builds the Vue frontend with Node 22 Alpine. Stage 2 installs Python deps into a virtualenv. Stage 3 assembles the final image with Python 3.11-slim-bookworm, installs Playwright Chromium, and copies all artifacts. Uses tini as the process supervisor.

3. **web-ui/ directory**: Standard Vite/Vue 3 project. The `npm run build` command outputs to `../dist/` relative to the web-ui directory, which resolves to `/dist` in the Node build context.

4. **src/ directory**: FastAPI application with spider logic, LLM integration, and static file serving for the Vue build.

5. **requirements-runtime.txt**: Lists fastapi, playwright, openai, and related packages with minimum version constraints.

## Decisions Made

### Used the existing Dockerfile structure

The upstream Dockerfile is well-designed. The multi-stage approach correctly separates the Node build, the Python venv build, and the final runtime image. No architectural changes were needed.

### Removed the Chinese PyPI mirror

The upstream Dockerfile passed `-i https://pypi.tuna.tsinghua.edu.cn/simple` to pip install. This mirror is a reliability dependency on a third-party Chinese service. For our international deployment environment, removing it and using the default PyPI index is more reliable and removes an unnecessary external dependency from the supply chain.

### Fixed the Vue build output COPY path

The upstream Dockerfile contained `COPY --from=frontend-builder /web-ui/dist /app/dist`. This path is incorrect. The Vite build in the frontend-builder stage runs with WORKDIR /web-ui, and the vite.config.js sets the build output to `../dist` (relative to the web-ui directory), which means the built files land at `/dist` in the container, not `/web-ui/dist`. The fix is `COPY --from=frontend-builder /dist /app/dist`. Without this fix, the COPY instruction silently copies nothing (Docker does not error on empty COPY from a build stage), and the Vue frontend is absent from the final image.

### Kept root user

The upstream Dockerfile explicitly sets `USER root` before the entrypoint. The Playwright browser management and some spider operations require root. This is an upstream architectural decision and was preserved per the architectural fidelity rule.

### Kept timezone set to Asia/Shanghai

The TZ environment variable is set to Asia/Shanghai in the upstream. This is relevant because Xianyu is a Chinese platform and timestamps in listings are in CST. Changing this could affect time-based filtering logic in the application.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. All three stages completed. Node build produced the dist directory. Playwright Chromium installed without issues on linux/amd64.
2. **FastAPI import**: `python -c "import fastapi"` passed.
3. **Container startup**: Container started and the FastAPI server bound to port 8000.

### What Was Not Tested
- Actual Xianyu scraping (requires a logged-in Xianyu session and a valid OpenAI vision API key)
- LLM price extraction (requires OPENAI_API_KEY with a vision-capable model)
- Vue frontend rendering in browser (requires running container with correct config)

## Gotchas

1. **Vite output path**: As described above, the COPY path in the upstream Dockerfile was wrong. This is a silent failure in Docker multi-stage builds. Always verify the actual output path of frontend build tools.

2. **Playwright in Docker**: The `--with-deps --no-shell` flags are important. `--with-deps` installs all system libraries Chromium needs. `--no-shell` skips the shell browser which is not needed.

3. **Xianyu login session**: The app requires a Xianyu account. The session state is stored in `/app/state`. Without a valid session, all scraping requests will fail with authentication errors from Xianyu.

4. **Vision model requirement**: The OPENAI_MODEL_NAME must be a model that supports image input. Text-only models will fail at the screenshot analysis step.

# hcaptcha-challenger. Reasoning Log

## Initial Assessment

hcaptcha-challenger is a Python tool for programmatically solving hCaptcha challenges. It uses Playwright (via Camoufox, a fingerprint-spoofing browser wrapper) to interact with challenge pages, and relies on Google Gemini vision models to classify challenge images. It supports three modes: CLI invocation, a FastAPI server for remote solve requests, and a dataset collection mode.

## What Was Checked

1. **README.md**: Describes installation via uv with multiple extras (server, camoufox, dataset). Shows CLI usage with the `hc` command. Mentions environment variables for Gemini API key.

2. **pyproject.toml**: Defines three optional extras. The project uses uv for package management with a lock file. Python 3.11+ required.

3. **uv.lock**: Frozen lock file covering all three extras. Includes playwright, camoufox, fastapi, and the hcaptcha_challenger package itself.

4. **Upstream Dockerfile**: None existed. The Dockerfile was written for this deployment.

5. **src/hcaptcha_challenger/**: Source package. Contains the CLI entry point (`hc`), server module, and challenge-solving logic using Gemini API calls.

## Decisions Made

### Used Microsoft Playwright base image

The `mcr.microsoft.com/playwright/python` image is the official base for Playwright Python projects. It pre-installs all browser dependencies and Playwright browsers. Using this image avoids the complexity of manually installing Chromium and its system library dependencies, which vary across Debian/Ubuntu versions and are notoriously difficult to get right in slim images.

### Added Xvfb for headless display

Camoufox requires a display (even in headless mode, it initializes a display context that is different from Playwright's pure headless mode). Xvfb provides a virtual framebuffer that satisfies this requirement. All browser invocations must be wrapped with `xvfb-run`.

### Installed all extras with uv sync

The `--all-extras` flag installs server, camoufox, and dataset extras together. This produces a single image that supports all operational modes without needing to rebuild for different use cases. The image is larger but more flexible for research purposes.

### Set DISPLAY=:99 as default environment variable

This ensures that any process spawned inside the container that requires a display will use the Xvfb display started by `xvfb-run`. Without this, processes may fail with "cannot connect to X server" errors.

### Kept Camoufox GeoIP fetch at build time

The `uv run camoufox fetch` command downloads GeoIP data used for browser fingerprinting. Fetching at build time means the data is bundled in the image and no network access is needed at runtime for fingerprinting functionality.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. uv sync resolved all dependencies from the frozen lock file. Playwright browsers installed. Camoufox GeoIP data fetched.
2. **CLI help**: `xvfb-run --auto-servernum hc --help` ran successfully and printed usage information.
3. **Default CMD**: Container started and ran the default `hc --help` command without error.

### What Was Not Tested
- Actual hCaptcha solving (requires a live challenge page and GEMINI_API_KEY)
- FastAPI server mode (requires starting the server explicitly)
- Dataset collection mode

## Gotchas

1. **uv virtual environment path**: uv installs packages into a virtual environment at `/app/.venv`. The `hc` CLI binary is placed in `/app/.venv/bin/hc`. The Dockerfile does not add this to PATH, so direct `hc` invocations work via uv's shim mechanism but `python -c "import hcaptcha_challenger"` using the system Python will fail because the system Python does not see the venv. Use `uv run python -c "import hcaptcha_challenger"` for Python-level checks. This is why the healthcheck is a conditional OR: it tries the import first and falls back to `hc --help`.

2. **Xvfb required**: Any browser automation command must be prefixed with `xvfb-run --auto-servernum`. Omitting this causes Camoufox to fail when trying to initialize the display.

3. **Gemini API key required for solving**: The tool does not have a fallback solver. Without a valid GEMINI_API_KEY, all challenge classification steps will fail with an API authentication error.

4. **Base image size**: The Microsoft Playwright image is large (several GB) because it includes full browser builds. This is expected and acceptable for a research deployment.

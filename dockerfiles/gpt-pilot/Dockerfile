# Custom slim CLI Dockerfile for gpt-pilot (pythagora-core v2.0.10)
# The upstream Dockerfile requires a proprietary VSIX extension and builds a full
# code-server (VS Code in browser) image. This image ships only the CLI core.

FROM python:3.12-slim

# System deps: git (gpt-pilot shells out to git), build-essential (C extensions
# such as tiktoken and greenlet need a compiler)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd -m -u 1000 pilot

WORKDIR /app

# Install Python deps before copying app code so this layer is cached on
# code-only changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY --chown=pilot:pilot . .

# Persistent SQLite data lives here; mount a named volume to survive restarts
VOLUME ["/app/data"]

USER pilot

# Import-based healthcheck -- verifies the core package is importable without
# starting a project or touching the network
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "from core.agents.orchestrator import Orchestrator"

ENTRYPOINT ["python", "main.py"]

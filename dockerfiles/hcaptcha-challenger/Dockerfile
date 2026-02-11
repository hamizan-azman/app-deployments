FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

RUN pip install --no-cache-dir uv && \
    ln -sf /usr/local/bin/uv /bin/uv && \
    ln -sf /usr/local/bin/uvx /bin/uvx

USER root

WORKDIR /app

SHELL ["/bin/bash", "-c"]

ENV UV_LINK_MODE=copy \
    DISPLAY=:99

# Install system deps: xvfb for headless display, tini as init
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    xvfb \
    tini \
    wget \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Copy project files needed for uv sync
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

# Install Python dependencies (all extras: server, camoufox, dataset)
RUN uv sync --frozen --no-cache --all-extras

# Install Playwright browsers with system deps
RUN uv run playwright install --with-deps

# Install Camoufox GeoIP data
RUN uv run camoufox fetch

# Copy remaining project files
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import hcaptcha_challenger" || hc --help

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["sh", "-c", "xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1920x1080x24' hc --help"]

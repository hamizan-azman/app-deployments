# Build stage
FROM python:3.11.12-slim AS builder

# Install uv
RUN pip install --no-cache-dir uv && ln -s /usr/local/bin/uv /bin/uv && ln -s /usr/local/bin/uvx /bin/uvx

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cmake \
    python3-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (required for morphik-rust path dependency)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# uv environment
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/root/.cache/uv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"

# Copy project definition and local path dependencies before syncing
COPY pyproject.toml uv.lock ./
COPY fde ./fde
COPY morphik_rust ./morphik_rust

# Install CPU-only torch first (lock file has CUDA deps that don't resolve)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install all dependencies except the project itself (layer cache)
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --verbose --no-install-project || \
    uv pip install -r pyproject.toml --no-deps 2>/dev/null || true

# Copy full source
COPY . .
COPY ee/ui-component /app/ee/ui-component

# Install the project in non-editable mode
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --verbose --locked --no-editable

# Enable backports and install GCC 11+ for Debian Bookworm
RUN echo "deb http://deb.debian.org/debian bookworm-backports main" > /etc/apt/sources.list.d/backports.list && \
    apt-get update && \
    apt-get install -y -t bookworm-backports gcc-11 g++-11 && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100

# Production stage
FROM python:3.11.12-slim

WORKDIR /app

# Runtime system dependencies
# LibreOffice: ColPali processing of Office docs (docx/xlsx/pptx -> PDF -> images)
# poppler-utils: PDF utilities
# ffmpeg: audio/video processing
# curl: HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libmagic1 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi8 \
    libxml2 \
    libxslt1.1 \
    libjpeg62-turbo \
    libopenjp2-7 \
    fonts-dejavu-core \
    postgresql-client \
    poppler-utils \
    gcc \
    g++ \
    cmake \
    python3-dev \
    git \
    curl \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    && rm -rf /var/lib/apt/lists/*

# Copy venv and uv binaries from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /bin/uvx /bin/uvx

# Copy local path dependencies
COPY --from=builder /app/fde ./fde
COPY --from=builder /app/morphik_rust ./morphik_rust

# Create storage and log directories
RUN mkdir -p storage logs

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:/usr/local/bin:${PATH}"

# Default config (overridden by volume mount at runtime)
COPY morphik.docker.toml /app/morphik.toml.default

# Entrypoint script: waits for PostgreSQL, then starts API or ARQ worker
COPY <<'EOF' /app/docker-entrypoint.sh
#!/bin/bash
set -e

# Use default config if no morphik.toml is mounted
if [ ! -f /app/morphik.toml ]; then
    cp /app/morphik.toml.default /app/morphik.toml
fi

# Wait for PostgreSQL when POSTGRES_URI is set
check_postgres() {
    if [ -n "$POSTGRES_URI" ]; then
        echo "Waiting for PostgreSQL..."
        max_retries=30
        retries=0
        until PGPASSWORD=$PGPASSWORD pg_isready -h postgres -U morphik -d morphik; do
            retries=$((retries + 1))
            if [ $retries -eq $max_retries ]; then
                echo "Error: PostgreSQL did not become ready in time"
                exit 1
            fi
            echo "Waiting for PostgreSQL... (Attempt $retries/$max_retries)"
            sleep 2
        done
        echo "PostgreSQL is ready."

        if ! PGPASSWORD=$PGPASSWORD psql -h postgres -U morphik -d morphik -c "SELECT 1" > /dev/null 2>&1; then
            echo "Error: Could not connect to PostgreSQL database"
            exit 1
        fi
        echo "PostgreSQL connection verified."
    fi
}

check_postgres

if [ $# -gt 0 ]; then
    exec "$@"
else
    exec uv run start_server.py --skip-redis-check
fi
EOF
RUN chmod +x /app/docker-entrypoint.sh

# Application source
COPY pyproject.toml uv.lock ./
COPY fde ./fde
COPY core ./core
COPY ee ./ee
COPY utils ./utils
COPY README.md LICENSE ./
COPY start_server.py ./

LABEL org.opencontainers.image.title="Morphik Core"
LABEL org.opencontainers.image.description="Morphik Core - document processing and retrieval system"
LABEL org.opencontainers.image.source="https://github.com/morphik-org/morphik-core"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

EXPOSE 8000

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]

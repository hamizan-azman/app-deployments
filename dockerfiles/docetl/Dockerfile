# Build stage for Python dependencies
FROM python:3.11-slim AS python-builder

RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
ENV DOCETL_HOME_DIR="/docetl-data"

WORKDIR /app

COPY pyproject.toml ./
COPY docetl/ ./docetl/
COPY server/ ./server/
COPY tests/ ./tests/
RUN touch README.md

RUN uv venv && \
    uv sync --all-extras

# Build stage for Node.js dependencies
FROM node:20-alpine AS node-builder

WORKDIR /app/website

ENV DOCETL_HOME_DIR="/docetl-data"

COPY website/package*.json ./
RUN npm install
COPY website/ ./
RUN npm run build

# Final runtime stage
FROM python:3.11-slim AS runtime

RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    DOCETL_HOME_DIR="/docetl-data"

COPY --from=python-builder /app/.venv ${VIRTUAL_ENV}

COPY docetl/ ./docetl/
COPY server/ ./server/
COPY tests/ ./tests/
COPY pyproject.toml ./
# .env is optional at build time; create an empty one if absent
RUN touch .env
COPY --from=node-builder /app/website ./website

ENV PORT=3000

RUN useradd -m -u 1000 appuser && \
    mkdir -p /docetl-data && \
    chown -R appuser:appuser /docetl-data /app

VOLUME ["/docetl-data"]

USER appuser

EXPOSE 3000 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["sh", "-c", "python3 server/app/main.py & cd website && npm run start"]

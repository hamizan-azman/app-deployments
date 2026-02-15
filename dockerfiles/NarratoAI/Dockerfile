# Multi-stage build - Build stage
FROM python:3.12-slim-bookworm AS builder

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    git-lfs \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim-bookworm

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /NarratoAI

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/NarratoAI" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
    imagemagick \
    ffmpeg \
    wget \
    curl \
    git-lfs \
    ca-certificates \
    dos2unix \
    && sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<policy domain="path" rights="read|write" pattern="@\*"/' /etc/ImageMagick-6/policy.xml || true \
    && git lfs install \
    && groupadd -r narratoai && useradd -r -g narratoai -d /NarratoAI -s /bin/bash narratoai \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=narratoai:narratoai docker-entrypoint.sh /usr/local/bin/
RUN dos2unix /usr/local/bin/docker-entrypoint.sh && chmod +x /usr/local/bin/docker-entrypoint.sh

COPY --chown=narratoai:narratoai . .

RUN mkdir -p storage/temp storage/tasks storage/json storage/narration_scripts storage/drama_analysis && \
    if [ ! -f config.toml ]; then cp config.example.toml config.toml; fi && \
    chown -R narratoai:narratoai /NarratoAI && \
    chmod -R 755 /NarratoAI

USER narratoai

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["webui"]

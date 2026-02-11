FROM python:3.12-slim-bookworm

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        git \
        libportaudio2 \
        pandoc && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user with UID 1000
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# Create virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Allow git to operate on mounted user project directories
RUN git config --system --add safe.directory /app

# Create required directories with correct ownership
RUN mkdir -p /home/appuser/.aider /home/appuser/.cache && \
    chown -R appuser:appuser /home/appuser /app /venv

# HOME points into /app so .aider cache persists in the mounted project dir
ENV HOME=/app

# Install aider-chat from PyPI (avoids setuptools-scm issues with submodules)
RUN /venv/bin/pip install --upgrade --no-cache-dir pip && \
    /venv/bin/pip install --no-cache-dir aider-chat

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["/venv/bin/aider", "--help"]

ENTRYPOINT ["/venv/bin/aider"]

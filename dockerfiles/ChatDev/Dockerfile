# ---- Builder: install deps with compilers and uv ----
FROM python:3.12-slim AS builder
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# System deps required to build Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    build-essential \
    python3-dev \
    libcairo2-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv for dependency resolution/install
RUN pip install --no-cache-dir uv

# Install the project virtualenv outside /app so bind-mounts don't hide it
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Copy dependency files first to maximize cache
COPY pyproject.toml ./
COPY uv.lock ./

# Create the project virtualenv and install deps
RUN uv sync --no-cache --frozen

# ---- Runtime: minimal image with only runtime libs + app ----
FROM python:3.12-slim AS runtime
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install only runtime system libraries (no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libcairo2 \
 && rm -rf /var/lib/apt/lists/*

# Copy the prebuilt virtualenv from the builder
COPY --from=builder /opt/venv /opt/venv

# Copy the rest of the application code
COPY . .

# Use the venv Python by default and keep Python output unbuffered
ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Drop privileges
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 6400

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:6400/docs')" || exit 1

CMD ["python", "server_main.py", "--port", "6400"]

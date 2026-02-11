FROM python:3.12-slim

WORKDIR /app

# Install Docker CLI for Docker-in-Docker
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io curl git \
    && rm -rf /var/lib/apt/lists/*

# Install magentic-ui from PyPI
RUN pip install --no-cache-dir magentic-ui

# App data directory
RUN mkdir -p /app/data

ENV INSIDE_DOCKER=1
ENV RUN_WITHOUT_DOCKER=False

EXPOSE 8081

ENTRYPOINT ["magentic-ui", "--host", "0.0.0.0", "--port", "8081", "--appdir", "/app/data", "--upgrade-database"]

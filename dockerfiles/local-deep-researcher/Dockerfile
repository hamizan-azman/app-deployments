FROM --platform=$BUILDPLATFORM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv
ENV PATH="/root/.local/bin:${PATH}"

COPY . /app

ENV OLLAMA_BASE_URL="http://localhost:11434/"

EXPOSE 2024

CMD ["uvx", \
     "--refresh", \
     "--from", "langgraph-cli[inmem]", \
     "--with-editable", ".", \
     "--python", "3.11", \
     "langgraph", \
     "dev", \
     "--host", "0.0.0.0"]

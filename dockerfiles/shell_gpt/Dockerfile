FROM python:3.11-slim

ENV SHELL_INTERACTION=false
ENV PRETTIFY_MARKDOWN=false
ENV OS_NAME=auto
ENV SHELL_NAME=auto

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir /app && mkdir -p /tmp/shell_gpt

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app /tmp/shell_gpt

VOLUME /tmp/shell_gpt

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD sgpt --help > /dev/null 2>&1 || exit 1

ENTRYPOINT ["sgpt"]

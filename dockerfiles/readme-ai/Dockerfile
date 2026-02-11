FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

ENV GIT_PYTHON_REFRESH=quiet

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir readmeai==0.6.3

RUN groupadd -r appuser && useradd -r -u 1000 -g appuser appuser

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import readmeai" || exit 1

ENTRYPOINT ["readmeai"]
CMD ["--help"]

FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        && \
    apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /Verba

COPY . /Verba

RUN pip install --no-cache-dir '.'

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /Verba

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

CMD ["verba", "start", "--port", "8000", "--host", "0.0.0.0"]

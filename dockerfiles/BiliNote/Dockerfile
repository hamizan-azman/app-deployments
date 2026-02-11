FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir ctranslate2==4.4.0 && pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/

RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

EXPOSE 8483

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8483/ || exit 1

CMD ["python", "main.py"]

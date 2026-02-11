FROM python:3.12-slim

RUN groupadd -r appuser && useradd -r -u 1000 -g appuser appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/config /app/report && \
    chown -R appuser:appuser /app && \
    chmod -R a+rw /usr/local/lib/python3.12/site-packages/efinance/ 2>/dev/null || true

VOLUME ["/app/config", "/app/report"]

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python main.py --help || python -c "import llm_adapters"

ENTRYPOINT ["python", "main.py"]

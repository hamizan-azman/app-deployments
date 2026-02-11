FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY dockerfiles/DeepGit/requirements.txt .

RUN pip install --upgrade pip setuptools wheel build && \
    pip install --no-cache-dir -r requirements.txt

COPY apps/DeepGit/ .

RUN chown -R appuser:appuser /app

USER appuser

ENV GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import gradio" || curl -f http://localhost:7860/

CMD ["python", "app.py"]

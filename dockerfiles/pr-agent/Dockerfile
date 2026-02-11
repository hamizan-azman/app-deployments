FROM python:3.12-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser pr_agent pr_agent

USER appuser

ENV PYTHONPATH=/app

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "from pr_agent import cli"

CMD ["python", "-m", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "pr_agent/servers/gunicorn_config.py", "--forwarded-allow-ips", "*", "--bind", "0.0.0.0:3000", "pr_agent.servers.github_app:app"]

FROM python:3.13-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY --chown=appuser:appuser . /app

RUN pip install --no-cache-dir .

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import zotero_arxiv_daily" || exit 1

ENTRYPOINT ["python", "-m", "zotero_arxiv_daily"]

FROM python:3.10-bookworm

WORKDIR /usr/src/vulnhuntr

RUN addgroup --gid 1000 appgroup && \
    adduser --uid 1000 --gid 1000 --disabled-password --gecos "" appuser

COPY . .
RUN pip install --no-cache-dir . && pip install --no-cache-dir requests

RUN chown -R appuser:appgroup /usr/src/vulnhuntr

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import vulnhuntr"

ENTRYPOINT ["vulnhuntr"]

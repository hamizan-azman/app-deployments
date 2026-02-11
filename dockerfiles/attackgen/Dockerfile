FROM python:3.12-slim

RUN groupadd -r attackgen && \
    useradd -r -g attackgen -u 1000 -m -d /home/attackgen attackgen

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip check

RUN mkdir -p /home/attackgen/.streamlit && \
    chown -R attackgen:attackgen /home/attackgen

COPY --chown=attackgen:attackgen . .

USER attackgen

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=2)" || exit 1

ENTRYPOINT ["streamlit", "run", "00_\ud83d\udc4b_Welcome.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.enableXsrfProtection=true"]

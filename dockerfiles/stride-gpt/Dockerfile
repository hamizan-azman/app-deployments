FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 -ms /bin/bash appuser && \
    pip install --no-cache-dir --upgrade pip && \
    mkdir -p /home/appuser/.local/bin /home/appuser/.local/lib

EXPOSE 8501

WORKDIR /home/appuser

COPY --chown=appuser:appuser . /home/appuser

USER appuser

ENV PATH="$PATH:/home/appuser/.local/bin:/home/appuser/.local/lib:/home/appuser/venv/bin"
ENV VIRTUAL_ENV=/home/appuser/venv

RUN python -m venv ${VIRTUAL_ENV}
RUN ${VIRTUAL_ENV}/bin/pip install --no-cache-dir -r requirements.txt && \
    ${VIRTUAL_ENV}/bin/pip check

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=2)" || exit 1

ENTRYPOINT ["streamlit", "run", "main.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.enableXsrfProtection=true"]

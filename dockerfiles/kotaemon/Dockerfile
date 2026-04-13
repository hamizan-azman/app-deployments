FROM python:3.10-slim AS lite

RUN apt-get update -qqy && \
    apt-get install -y --no-install-recommends \
        ssh \
        git \
        gcc \
        g++ \
        poppler-utils \
        libpoppler-dev \
        unzip \
        curl \
        wget \
        cargo \
        && \
    apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG TARGETPLATFORM
ARG TARGETARCH

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV TARGETARCH=${TARGETARCH}
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

WORKDIR /app

COPY scripts/download_pdfjs.sh /app/scripts/download_pdfjs.sh
RUN chmod +x /app/scripts/download_pdfjs.sh
ENV PDFJS_PREBUILT_DIR="/app/libs/ktem/ktem/assets/prebuilt/pdfjs-dist"
RUN bash scripts/download_pdfjs.sh $PDFJS_PREBUILT_DIR

RUN pip install --no-cache-dir "uv"

COPY . /app
COPY launch.sh /app/launch.sh
RUN sed -i 's/\r$//' /app/launch.sh
COPY .env.example /app/.env

RUN uv sync --frozen --no-cache \
    && uv pip install --python .venv "pdfservices-sdk@git+https://github.com/niallcm/pdfservices-python-sdk.git@bump-and-unfreeze-requirements"

RUN if [ "$TARGETARCH" = "amd64" ]; then uv pip install --python .venv "graphrag<=0.3.6" future; fi

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/')" || exit 1

ENTRYPOINT ["sh", "/app/launch.sh"]

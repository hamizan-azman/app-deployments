FROM python:3.11-slim-bullseye

WORKDIR /MoneyPrinterTurbo

RUN chmod 777 /MoneyPrinterTurbo

ENV PYTHONPATH="/MoneyPrinterTurbo"

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        imagemagick \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick security policy that blocks PDF/text operations used by moviepy
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml

COPY requirements.txt ./

RUN pip install --no-cache-dir --retries 3 --timeout 60 -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /MoneyPrinterTurbo
USER appuser

EXPOSE 8501 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import streamlit"

# Default: run the Streamlit webui. Override CMD in docker-compose for the API service.
CMD ["streamlit", "run", "./webui/Main.py", \
     "--browser.serverAddress=0.0.0.0", \
     "--server.enableCORS=True", \
     "--browser.gatherUsageStats=False"]

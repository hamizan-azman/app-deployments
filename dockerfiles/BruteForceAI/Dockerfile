FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY dockerfiles/BruteForceAI/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN playwright install chromium

COPY apps/BruteForceAI/ /app/

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python BruteForceAI.py --help || python -c "import playwright"

ENTRYPOINT ["python", "BruteForceAI.py"]

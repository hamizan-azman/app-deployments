FROM python:3.12-slim

RUN useradd -m -u 1000 user

RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=user ./sparrow-ml/llm/requirements_sparrow_parse.txt requirements_sparrow_parse.txt
RUN pip install --no-cache-dir --upgrade -r requirements_sparrow_parse.txt

COPY --chown=user ./sparrow-ml/llm /app

USER user

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/docs')" || exit 1

CMD ["python", "api.py", "--port", "7860"]

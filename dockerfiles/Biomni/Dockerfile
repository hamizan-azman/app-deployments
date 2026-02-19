FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY biomni ./biomni

RUN pip install --no-cache-dir -e ".[gradio]" \
    langchain-openai langchain-anthropic langchain-text-splitters

RUN mkdir -p /app/data

COPY entrypoint.py .

EXPOSE 7860

CMD ["python", "entrypoint.py"]

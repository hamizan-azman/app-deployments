FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir codeqai faiss-cpu

# Pre-create config for OpenAI (bypasses interactive codeqai configure)
RUN mkdir -p /root/.config/codeqai && \
    printf 'embeddings: OpenAI-text-embedding-ada-002\nllm-host: OpenAI\nchat-model: gpt-4o-mini\n' > /root/.config/codeqai/config.yaml

# Set up sample git repo using codeqai source as demo project
WORKDIR /app/sample-project
COPY codeqai/ ./codeqai/
COPY pyproject.toml ./
RUN git config --global user.email "docker@example.com" && \
    git config --global user.name "Docker" && \
    git init && git add -A && git commit -m "Initial commit"

# Streamlit config for Docker
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8501

CMD ["codeqai", "app"]

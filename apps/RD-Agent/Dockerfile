FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 19899

ENTRYPOINT ["rdagent"]
CMD ["--help"]

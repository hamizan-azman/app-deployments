FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    && curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-27.4.1.tgz | tar xz --strip-components=1 -C /usr/local/bin docker/docker \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY gpt_migrate/requirements.txt /app/requirements.txt

# Era-matched pins for mid-2023 deps
# Install typer first without typer-slim to avoid version conflict
RUN pip install --no-cache-dir \
    typer==0.9.0 \
    click==8.1.7 \
    && pip install --no-cache-dir \
    openai==0.27.8 \
    langchain==0.0.238 \
    litellm==0.1.213 \
    pydantic==1.10.8 \
    yaspin==2.5.0 \
    tree-sitter==0.20.4

COPY . /app

WORKDIR /app/gpt_migrate

ENTRYPOINT ["python", "main.py"]

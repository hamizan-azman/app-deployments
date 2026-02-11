FROM python:3.11 AS requirements-stage

WORKDIR /tmp
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && ln -s /root/.local/bin/uv /usr/local/bin/uv
COPY ./pyproject.toml /tmp/pyproject.toml
COPY ./uv.lock /tmp/uv.lock
RUN uv pip compile pyproject.toml -o requirements.txt --no-annotate --no-header

FROM python:3.11-slim-bookworm
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN playwright install-deps
RUN playwright install
RUN apt-get update && apt-get install -y xauth x11-apps netpbm gpg ca-certificates x11vnc xterm x11-utils && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir websockify

COPY .nvmrc /app/.nvmrc
COPY nodesource-repo.gpg.key /tmp/nodesource-repo.gpg.key
RUN cat /tmp/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    NODE_MAJOR=$(cut -d. -f1 < /app/.nvmrc) && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" >> /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/nodesource-repo.gpg.key && \
    npm -v && node -v

# Install bitwarden CLI
RUN npm install -g @bitwarden/cli@2025.9.0
# Checking bw version also initializes the bw config
RUN bw --version

COPY . /app

ENV PYTHONPATH="/app"
ENV VIDEO_PATH=/data/videos
ENV HAR_PATH=/data/har
ENV LOG_PATH=/data/log
ENV ARTIFACT_STORAGE_PATH=/data/artifacts

# Cache tiktoken encodings at build time
RUN python /app/scripts/load_tiktoken.py

COPY ./entrypoint-skyvern.sh /app/entrypoint-skyvern.sh
RUN sed -i 's/\r$//' /app/entrypoint-skyvern.sh && chmod +x /app/entrypoint-skyvern.sh

EXPOSE 8000 6080 9222

HEALTHCHECK --interval=15s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["/bin/bash", "/app/entrypoint-skyvern.sh"]

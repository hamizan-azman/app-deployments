FROM python:3.12-slim-bookworm AS install-browser

RUN apt-get update \
    && apt-get install -y gnupg wget ca-certificates --no-install-recommends \
    && ARCH=$(dpkg --print-architecture) \
    && wget -qO - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=${ARCH}] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y chromium chromium-driver \
    && chromium --version && chromedriver --version \
    && apt-get install -y --no-install-recommends firefox-esr build-essential \
    && GECKO_ARCH=$(case ${ARCH} in amd64) echo "linux64" ;; arm64) echo "linux-aarch64" ;; *) echo "linux64" ;; esac) \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-${GECKO_ARCH}.tar.gz \
    && tar -xvzf geckodriver-v0.36.0-${GECKO_ARCH}.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.36.0-${GECKO_ARCH}.tar.gz \
    && rm -rf /var/lib/apt/lists/*

FROM install-browser AS gpt-researcher-install

ENV PIP_ROOT_USER_ACTION=ignore
WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt
COPY ./multi_agents/requirements.txt ./multi_agents/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --upgrade --prefer-binary && \
    pip install --no-cache-dir -r multi_agents/requirements.txt --upgrade --prefer-binary

FROM gpt-researcher-install AS gpt-researcher

ARG HOST=0.0.0.0
ENV HOST=${HOST}
ARG PORT=8000
ENV PORT=${PORT}
EXPOSE ${PORT}

ARG WORKERS=1
ENV WORKERS=${WORKERS}

RUN useradd -ms /bin/bash gpt-researcher && \
    chown -R gpt-researcher:gpt-researcher /usr/src/app && \
    mkdir -p /usr/src/app/outputs && \
    chown -R gpt-researcher:gpt-researcher /usr/src/app/outputs && \
    chmod 777 /usr/src/app/outputs
USER gpt-researcher
WORKDIR /usr/src/app

COPY --chown=gpt-researcher:gpt-researcher ./ ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

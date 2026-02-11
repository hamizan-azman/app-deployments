# syntax=docker/dockerfile:1
# check=skip=SecretsUsedInArgOrEnv

# Dockerfile for browser-use (hoomzoom/browser-use)
# Adapted from upstream Dockerfile. Minimal changes:
#   - Removed --mount=type=cache directives (BuildKit cache mounts unreliable on Windows/WSL2)
#   - EXPOSE 9242 9222 already present in upstream; preserved as-is
# All other structure, user setup, chromium apt install, and uv approach kept exactly as upstream.

FROM python:3.12-slim

LABEL name="browseruse" \
    maintainer="Nick Sweeting <dockerfile@browser-use.com>" \
    description="Make websites accessible for AI agents. Automate tasks online with ease." \
    homepage="https://github.com/browser-use/browser-use" \
    documentation="https://docs.browser-use.com" \
    org.opencontainers.image.title="browseruse" \
    org.opencontainers.image.vendor="browseruse" \
    org.opencontainers.image.description="Make websites accessible for AI agents. Automate tasks online with ease." \
    org.opencontainers.image.source="https://github.com/browser-use/browser-use" \
    com.docker.image.source.entrypoint="Dockerfile"

ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

######### Environment Variables #################################

# Global system-level config
ENV TZ=UTC \
    LANGUAGE=en_US:en \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_PREFERENCE=only-system \
    npm_config_loglevel=error \
    IN_DOCKER=True

# User config
ENV BROWSERUSE_USER="browseruse" \
    DEFAULT_PUID=911 \
    DEFAULT_PGID=911

# Paths
ENV CODE_DIR=/app \
    DATA_DIR=/data \
    VENV_DIR=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Build shell config
SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "errtrace", "-o", "nounset", "-c"]

# Force apt to leave downloaded binaries in /var/cache/apt (massively speeds up Docker builds)
RUN echo 'Binary::apt::APT::Keep-Downloaded-Packages "1";' > /etc/apt/apt.conf.d/99keep-cache \
    && echo 'APT::Install-Recommends "0";' > /etc/apt/apt.conf.d/99no-intall-recommends \
    && echo 'APT::Install-Suggests "0";' > /etc/apt/apt.conf.d/99no-intall-suggests \
    && rm -f /etc/apt/apt.conf.d/docker-clean

# Print debug info about build and save it to disk
RUN (echo "[i] Docker build for Browser Use starting..." \
    && echo "PLATFORM=${TARGETPLATFORM} ARCH=$(uname -m) ($(uname -s) ${TARGETARCH} ${TARGETVARIANT})" \
    && echo "BUILD_START_TIME=$(date +"%Y-%m-%d %H:%M:%S %s") TZ=${TZ} LANG=${LANG}" \
    && echo \
    && echo "CODE_DIR=${CODE_DIR} DATA_DIR=${DATA_DIR} PATH=${PATH}" \
    && echo \
    && uname -a \
    && cat /etc/os-release | head -n7 \
    && which bash && bash --version | head -n1 \
    && which dpkg && dpkg --version | head -n1 \
    && echo -e '\n\n' && env && echo -e '\n\n' \
    && which python && python --version \
    && which pip && pip --version \
    && echo -e '\n\n' \
    ) | tee -a /VERSION.txt

# Create non-privileged user for browseruse and chrome
RUN echo "[*] Setting up $BROWSERUSE_USER user uid=${DEFAULT_PUID}..." \
    && groupadd --system $BROWSERUSE_USER \
    && useradd --system --create-home --gid $BROWSERUSE_USER --groups audio,video $BROWSERUSE_USER \
    && usermod -u "$DEFAULT_PUID" "$BROWSERUSE_USER" \
    && groupmod -g "$DEFAULT_PGID" "$BROWSERUSE_USER" \
    && mkdir -p /data \
    && mkdir -p /home/$BROWSERUSE_USER/.config \
    && chown -R $BROWSERUSE_USER:$BROWSERUSE_USER /home/$BROWSERUSE_USER \
    && ln -s $DATA_DIR /home/$BROWSERUSE_USER/.config/browseruse \
    && echo -e "\nBROWSERUSE_USER=$BROWSERUSE_USER PUID=$(id -u $BROWSERUSE_USER) PGID=$(id -g $BROWSERUSE_USER)\n\n" \
    | tee -a /VERSION.txt

# Install base apt dependencies
RUN apt-get update -qq \
    && apt-get install -qq -y --no-install-recommends \
        apt-transport-https ca-certificates apt-utils gnupg2 unzip curl wget grep \
        nano iputils-ping dnsutils jq \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv && ln -sf /usr/local/bin/uv /bin/uv && ln -sf /usr/local/bin/uvx /bin/uvx

# Copy only dependency manifest
WORKDIR /app
COPY pyproject.toml uv.lock* /app/

RUN echo "[+] Setting up venv using uv in $VENV_DIR..." \
    && ( \
     which uv && uv --version \
     && uv venv \
     && which python | grep "$VENV_DIR" \
     && python --version \
    ) | tee -a /VERSION.txt

# Install Chromium browser directly from system packages
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        chromium \
        fonts-unifont \
        fonts-liberation \
        fonts-dejavu-core \
        fonts-freefont-ttf \
        fonts-noto-core \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/chromium /usr/bin/chromium-browser \
    && ln -s /usr/bin/chromium /app/chromium-browser \
    && mkdir -p "/home/${BROWSERUSE_USER}/.config/chromium/Crash Reports/pending/" \
    && chown -R "$BROWSERUSE_USER:$BROWSERUSE_USER" "/home/${BROWSERUSE_USER}/.config" \
    && ( \
        which chromium-browser && /usr/bin/chromium-browser --version \
        && echo -e '\n\n' \
    ) | tee -a /VERSION.txt

RUN echo "[+] Installing browser-use pip sub-dependencies..." \
    && ( \
       uv sync --all-extras --no-dev --no-install-project \
       && echo -e '\n\n' \
    ) | tee -a /VERSION.txt

# Copy the rest of the browser-use codebase
COPY . /app

# Install the browser-use package and all of its optional dependencies
RUN echo "[+] Installing browser-use pip library from source..." \
    && ( \
       uv sync --all-extras --locked --no-dev \
       && python -c "import browser_use; print('browser-use installed successfully')" \
       && echo -e '\n\n' \
    ) | tee -a /VERSION.txt

RUN mkdir -p "$DATA_DIR/profiles/default" \
    && chown -R $BROWSERUSE_USER:$BROWSERUSE_USER "$DATA_DIR" "$DATA_DIR"/* \
    && ( \
        echo -e "\n\n[√] Finished Docker build successfully. Saving build summary in: /VERSION.txt" \
        && echo -e "PLATFORM=${TARGETPLATFORM} ARCH=$(uname -m) ($(uname -s) ${TARGETARCH} ${TARGETVARIANT})\n" \
        && echo -e "BUILD_END_TIME=$(date +"%Y-%m-%d %H:%M:%S %s")\n\n" \
    ) | tee -a /VERSION.txt


USER "$BROWSERUSE_USER"
VOLUME "$DATA_DIR"
EXPOSE 9242
EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD browser-use --help > /dev/null 2>&1 || exit 1

ENTRYPOINT ["browser-use"]

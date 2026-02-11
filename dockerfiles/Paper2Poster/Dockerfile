FROM ubuntu:24.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Configure apt to use multiple mirrors and retry
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries && \
    echo 'Acquire::http::Timeout "30";' >> /etc/apt/apt.conf.d/80-retries && \
    echo 'Acquire::ftp::Timeout "30";' >> /etc/apt/apt.conf.d/80-retries

# Update package list with retries and install system dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y --fix-missing --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    libreoffice \
    default-jre \
    poppler-utils \
    git \
    curl \
    ca-certificates \
    libgl1 \
    libglib2.0-0t64 \
    libgomp1 \
    fonts-dejavu \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create a symbolic link for python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy local repository contents (includes latest fixes)
COPY . .

# Upgrade pip; constrain setuptools<71 in build isolation only (pkg_resources removed in 71+)
RUN python3 -m pip install --no-cache-dir --break-system-packages --ignore-installed pip && \
    echo "setuptools<71" > /tmp/build-constraints.txt
ENV PIP_BUILD_CONSTRAINT=/tmp/build-constraints.txt

# Install full Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Create data directory for mounting
RUN mkdir -p /data

# Create startup script
RUN echo '#!/bin/bash\necho "OPENAI_API_KEY=$OPENAI_API_KEY" > /app/.env\ncd /app\nexport PYTHONPATH=/app:$PYTHONPATH\nexec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command (can be overridden)
CMD ["python", "-m", "PosterAgent.new_pipeline", "--help"]

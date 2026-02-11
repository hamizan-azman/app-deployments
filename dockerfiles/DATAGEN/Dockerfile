FROM python:3.10-slim

# Install system deps and Google Chrome (Chrome deb pulls in all needed libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg curl unzip ca-certificates \
    && wget -q -O /tmp/google-chrome.deb \
        https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y /tmp/google-chrome.deb \
    && rm /tmp/google-chrome.deb \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver via Chrome for Testing
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1) \
    && CHROMEDRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget -q -O /tmp/chromedriver.zip \
        "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_URL}/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy and install pinned requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY --chown=appuser:appuser . /app/

# Set ChromeDriver path as used in .env Example
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV WORKING_DIRECTORY=/app/data/

# Create data directory
RUN mkdir -p /app/data && chown appuser:appuser /app/data

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import langchain"

CMD ["python", "main.py"]

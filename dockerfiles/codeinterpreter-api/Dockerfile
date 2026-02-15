FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install the library with all extras (includes local codebox support, streamlit frontend, image support)
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/

RUN pip install --no-cache-dir ".[all]"

# Copy examples for reference
COPY examples/ examples/

# Keep container running for interactive use
CMD ["python", "-c", "from codeinterpreterapi import CodeInterpreterSession, File, settings; print('codeinterpreterapi imported successfully. Ready for use. Set OPENAI_API_KEY to run sessions.')"]

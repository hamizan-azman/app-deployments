FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-wqy-zenhei fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

# Pre-install era-matched pins for packages that cause build/resolution issues
RUN pip install --no-cache-dir \
    scikit-learn==1.1.3 scipy==1.7.3 typing_extensions==4.7.1 \
    "pydantic<2" "gradio==3.35.2" "gradio-client==0.2.7"

# Install requirements WITH deps, skip already-pinned and zhipuai (pydantic v2 conflict)
COPY requirements.txt .
RUN sed -i '/scikit-learn/d; /typing_extensions/d; /scipy/d; /zhipuai/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "pydantic<2"

COPY . .

# Patch: zhipuai v2 requires pydantic v2 which conflicts with gradio 3.x
# Make the import graceful so the app starts (GLM features unavailable without zhipuai)
COPY patch_zhipuai.py /tmp/patch_zhipuai.py
RUN python3 /tmp/patch_zhipuai.py && rm /tmp/patch_zhipuai.py

ENV GRADIO_SERVER_NAME=0.0.0.0
EXPOSE 7860

CMD ["python", "app.py"]

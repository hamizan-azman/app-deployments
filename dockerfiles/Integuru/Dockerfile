FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-interaction

RUN playwright install --with-deps chromium

COPY . .
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["integuru"]

# Stage 1: Build frontend
FROM node:20-slim AS frontend-build

WORKDIR /build
RUN npm install -g pnpm

COPY example/package.json example/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY example/assets ./assets
COPY example/webpack.config.js example/babel.config.js example/postcss.config.cjs example/tsconfig.json ./
COPY frontend ../frontend

# Build with production publicPath
RUN sed -i 's|publicPath: "http://localhost:3000/webpack_bundles/"|publicPath: "/static/webpack_bundles/"|' webpack.config.js && \
    npx webpack --mode=production

# Stage 2: Python backend
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git libxml2-dev libxslt1-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Install library deps
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-interaction

# Install example deps
RUN pip install --no-cache-dir django-webpack-loader requests lxml wikipedia \
    langchain-anthropic langchain-community langchain-text-splitters \
    gitpython scikit-learn pycmarkgfm gunicorn python-dotenv

# Copy source and install the library package
COPY django_ai_assistant ./django_ai_assistant
COPY example ./example
COPY README.md pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir -e .

# Copy built frontend from stage 1
COPY --from=frontend-build /build/assets/webpack_bundles ./example/assets/webpack_bundles
COPY --from=frontend-build /build/webpack-stats.json ./example/webpack-stats.json

WORKDIR /app/example

# Run migrations + collectstatic + create superuser
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=example.settings
RUN python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput 2>/dev/null || true && \
    python -c "import django; django.setup(); from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@test.com', 'admin') if not User.objects.filter(username='admin').exists() else None"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

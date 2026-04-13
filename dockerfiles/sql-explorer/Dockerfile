# Build stage
FROM python:3.12.4 as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/dev.txt

# Install NVM and Node.js
RUN mkdir /usr/local/.nvm
ENV NVM_DIR /usr/local/.nvm
ENV NODE_VERSION 20.15.1

COPY package.json package-lock.json /app/

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install ${NODE_VERSION} \
    && nvm use v${NODE_VERSION} \
    && nvm alias default v${NODE_VERSION} \
    && npm install


# Runtime stage
FROM python:3.12.4

WORKDIR /app

# Install curl for HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --uid 1000 appuser

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy Node.js environment from builder
COPY --from=builder /usr/local/.nvm /usr/local/.nvm
ENV NVM_DIR /usr/local/.nvm
ENV PATH $NVM_DIR/versions/node/v20.15.1/bin:$PATH

COPY --from=builder /app/node_modules /app/node_modules

COPY . /app

# Fix Windows line endings on entrypoint script
RUN sed -i 's/\r$//' /app/entrypoint.sh

# Run migrations and create initial data
RUN python manage.py migrate && \
    python manage.py shell <<ORM
from django.contrib.auth.models import User
u = User.objects.filter(username='admin').first()
if not u:
    u = User(username='admin')
    u.set_password('admin')
    u.is_superuser = True
    u.is_staff = True
    u.save()

from explorer.models import Query
queries = Query.objects.all().count()
if queries == 0:
    q = Query(sql='select * from explorer_query;', title='Sample Query')
    q.save()
ORM

# Copy and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && sed -i 's/\r$//' /entrypoint.sh

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000 5173

HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]

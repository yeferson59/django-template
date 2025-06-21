# Ultra-optimized multi-stage build for Django app
FROM python:3.13.3-alpine3.20 AS builder

# Install build dependencies in single layer
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    linux-headers \
    && pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with smart optimization
RUN uv sync --frozen --group prod --compile-bytecode --no-dev \
    && python -m compileall /app/.venv \
    && rm -rf /app/.venv/lib/python*/site-packages/pip* \
    && rm -rf /app/.venv/lib/python*/site-packages/setuptools* \
    && rm -rf /app/.venv/lib/python*/site-packages/wheel* \
    && find /app/.venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true \
    && find /app/.venv -name "*.pyo" -delete 2>/dev/null || true \
    && apk del .build-deps

# Ultra-minimal production stage
FROM python:3.13.3-alpine3.20

# Install only essential runtime dependencies
RUN apk add --no-cache \
    libpq \
    && adduser -D -S appuser

WORKDIR /app

# Copy optimized Python environment
COPY --from=builder /app/.venv /app/.venv

# Copy only essential application files
COPY --chown=appuser manage.py ./
COPY --chown=appuser app/ ./app/
COPY --chown=appuser templates/ ./templates/
COPY --chown=appuser static/ ./static/

# Set environment variables in single layer
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=2 \
    DJANGO_SETTINGS_MODULE=app.settings_prod \
    PYTHONPATH=/app

# Collect static files and final cleanup
RUN python manage.py collectstatic --noinput \
    && find /app -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true \
    && find /app -name "*.pyc" -delete 2>/dev/null || true

# Switch to non-root user
USER appuser

EXPOSE 8000

# Optimized gunicorn command
CMD ["gunicorn", "app.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--worker-class", "sync", \
     "--max-requests", "1000", \
     "--preload", \
     "--worker-connections", "1000", \
     "--timeout", "30"]

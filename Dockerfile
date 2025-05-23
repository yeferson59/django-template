# Multi-stage build for Django app with uv
FROM python:3.13.3-alpine3.20 AS builder

# Install build dependencies
RUN apk add --no-cache build-base

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install production dependencies only
RUN uv sync --frozen --group prod

# Production stage
FROM python:3.13.3-alpine3.20

# Install runtime dependencies only
RUN apk add --no-cache libgcc libstdc++ && \
    rm -rf /var/cache/apk/*

# Create non-root user
RUN adduser -D -H appuser

# Install uv in production stage
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Make sure we use venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=app.settings_prod

# Collect static files
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER appuser

EXPOSE 8000

# Use gunicorn with proper WSGI application
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

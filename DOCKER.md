# Docker Configuration for Django Application

## 🐳 Overview

This Django application uses an optimized multi-stage Docker build designed for production deployment with the following features:

- **Base Image**: Python 3.13.3 on Alpine Linux 3.20 (lightweight)
- **Package Manager**: UV (ultra-fast Python package management)
- **WSGI Server**: Gunicorn with 2 workers
- **Static Files**: WhiteNoise (no external web server required)
- **Security**: Non-root user execution
- **Final Image Size**: ~308MB (optimized for production)
- **Build Architecture**: Multi-stage build for minimal production footprint

## 🚀 Quick Start

### Build and Run Commands

```bash
# Build the production image
docker build -t my-django-app .

# Run with development settings
docker run -p 8000:8000 -e DJANGO_SETTINGS_MODULE=app.settings my-django-app

# Run with production settings (default)
docker run -p 8000:8000 my-django-app

# Run with custom environment variables
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=yourdomain.com \
  my-django-app
```

### Using Docker Compose

```bash
# Development environment with hot reload
docker-compose up web

# Production environment testing
docker-compose up web-prod

# Staging environment
docker-compose up web-staging

# Full stack (web + database + redis)
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop all services
docker-compose down
```

## 📁 Project Structure

```
my-app/
├── Dockerfile                  # Multi-stage production build
├── docker-compose.yml          # Development/staging/production environments
├── .dockerignore              # Build optimization exclusions
├── app/
│   ├── settings.py            # Development settings
│   ├── settings_prod.py       # Production settings with security headers
│   ├── wsgi.py               # WSGI application entry point
│   └── asgi.py               # ASGI application entry point
├── tests/                     # Test suite
├── staticfiles/              # Collected static files (created during build)
├── pyproject.toml            # Dependencies with dev/prod groups
└── uv.lock                   # Locked dependencies for reproducible builds
```

## 🔧 Environment Variables

### Development Environment
```bash
DEBUG=true
DJANGO_SETTINGS_MODULE=app.settings
PYTHONUNBUFFERED=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Production Environment
```bash
DEBUG=false
DJANGO_SETTINGS_MODULE=app.settings_prod
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### Optional Database Configuration
```bash
# PostgreSQL (recommended for production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=db
DB_PORT=5432

# Or use DATABASE_URL
DATABASE_URL=postgres://user:password@host:port/database
```

### Optional Caching and Performance
```bash
# Redis for caching and sessions
REDIS_URL=redis://redis:6379/0

# Email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📦 Build Optimization Details

### Multi-stage Build Process

**Stage 1: Builder**
- Installs build dependencies (build-base)
- Uses UV to install Python dependencies
- Creates virtual environment with production packages only
- Excludes development tools and testing frameworks

**Stage 2: Production**
- Minimal Alpine base image
- Copies only the virtual environment from builder
- Installs runtime dependencies (libgcc, libstdc++)
- Creates non-root user for security
- Collects Django static files
- Configures production environment

### Optimization Features
- **Layer Caching**: Optimized layer order for faster rebuilds
- **Dependency Separation**: Production vs development dependency groups
- **Size Optimization**: Comprehensive .dockerignore excludes unnecessary files
- **Security**: Non-root user execution and minimal package installation
- **Performance**: UV package manager for faster dependency resolution

## 🛡️ Security Features

### Container Security
- **Non-root User**: Application runs as `appuser` (non-privileged)
- **Minimal Base**: Alpine Linux with only essential packages
- **No Development Tools**: Production image excludes dev dependencies
- **Security Headers**: HSTS, XSS protection, content type nosniff (in production settings)

### Django Security (Production)
- **Secure Cookies**: SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE enabled
- **HTTPS Enforcement**: Security middleware configured
- **Debug Mode**: Disabled in production
- **Secret Key**: Must be provided via environment variable

## 📊 Performance Characteristics

### Image Metrics
- **Final Image Size**: ~288MB
- **Build Time**: ~40 seconds (cold build) / ~10 seconds (with cache)
- **Workers**: 2 Gunicorn workers (configurable)
- **Memory Usage**: Low footprint with Alpine Linux base
- **Startup Time**: Fast application startup with optimized dependencies

### Runtime Performance
- **Static Files**: Served efficiently by WhiteNoise
- **Database**: SQLite for development, PostgreSQL recommended for production
- **Caching**: Redis support for session and application caching
- **Monitoring**: Gunicorn access logs and Django logging configured

## 🔄 Development Workflow

### Local Development with Docker
```bash
# Start development server with volume mounting
docker-compose up web

# Run management commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# View application logs
docker-compose logs -f web

# Execute shell in running container
docker-compose exec web /bin/sh
```

### Production Testing
```bash
# Test production build locally
docker-compose up web-prod

# Verify static files are served correctly
curl http://localhost:8001/static/admin/css/base.css

# Check application health
curl http://localhost:8001/admin/
```

### Database Integration
```bash
# Start with PostgreSQL database
docker-compose up web db

# Run migrations with database
docker-compose exec web python manage.py migrate

# Access database directly
docker-compose exec db psql -U myuser -d mydatabase
```

## 🚀 Production Deployment

### Registry Deployment
```bash
# Build and tag for registry
docker build -t my-django-app:latest .
docker tag my-django-app:latest registry.example.com/my-django-app:latest

# Push to container registry
docker push registry.example.com/my-django-app:latest

# Deploy from registry
docker run -d \
  --name django-prod \
  -p 80:8000 \
  -e SECRET_KEY=${SECRET_KEY} \
  -e ALLOWED_HOSTS=${ALLOWED_HOSTS} \
  registry.example.com/my-django-app:latest
```

### Environment Setup Checklist
1. ✅ Set production SECRET_KEY
2. ✅ Configure ALLOWED_HOSTS
3. ✅ Setup external database (PostgreSQL)
4. ✅ Configure Redis for caching (optional)
5. ✅ Setup SSL/TLS termination (load balancer/reverse proxy)
6. ✅ Configure logging and monitoring
7. ✅ Setup backup strategy for database
8. ✅ Configure email settings for notifications

### Recommended Production Stack
- **Orchestration**: Kubernetes, Docker Swarm, or ECS
- **Load Balancer**: nginx, Traefik, or cloud load balancer
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis for sessions and application cache
- **Monitoring**: Prometheus + Grafana or cloud monitoring
- **Logging**: Centralized logging with ELK stack or cloud logging
- **Backup**: Automated database backups and volume snapshots

## 🗂️ Static Files Management

### WhiteNoise Configuration
- Automatically serves static files without external web server
- Compresses CSS and JavaScript files
- Sets appropriate cache headers for performance
- Handles Django admin static files automatically

### Static Files Collection
```bash
# Static files are collected during Docker build
# Manual collection (if needed):
docker run --rm my-django-app python manage.py collectstatic --noinput

# Verify static files in container
docker run --rm my-django-app ls -la /app/staticfiles/
```

## 🔍 Troubleshooting

### Common Build Issues

**Build fails at dependency installation:**
```bash
# Clear Docker cache and rebuild
docker system prune -a
docker build --no-cache -t my-django-app .
```

**Permission denied errors:**
```bash
# Check file ownership in container
docker run --rm my-django-app ls -la /app/

# Verify non-root user is working
docker run --rm my-django-app whoami
```

**Static files not loading:**
```bash
# Verify WhiteNoise middleware is installed
docker run --rm my-django-app python -c "import whitenoise; print('WhiteNoise available')"

# Check static files collection
docker run --rm my-django-app python manage.py collectstatic --dry-run
```

### Runtime Debugging

**View container logs:**
```bash
# For Docker Compose
docker-compose logs -f web

# For standalone container
docker logs -f <container-name>
```

**Access container shell:**
```bash
# For Docker Compose
docker-compose exec web /bin/sh

# For standalone container
docker exec -it <container-name> /bin/sh
```

**Database connection issues:**
```bash
# Test database connectivity
docker-compose exec web python manage.py dbshell

# Verify database settings
docker-compose exec web python manage.py check --database default
```

### Performance Monitoring

**Container resource usage:**
```bash
# Monitor container resources
docker stats my-django-app

# View detailed container info
docker inspect my-django-app
```

**Application performance:**
```bash
# Enable Django Debug Toolbar in development
# Set DJANGO_DEBUG_TOOLBAR=true in environment

# Monitor Gunicorn worker processes
docker exec my-django-app ps aux | grep gunicorn
```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [UV Package Manager](https://github.com/astral-sh/uv)

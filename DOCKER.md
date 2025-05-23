# Docker Configuration for Django App

## 🐳 Overview

This Django application uses a multi-stage Docker build optimized for production with the following features:

- **Base Image**: Alpine Linux (lightweight)
- **Package Manager**: uv (fast Python package management)
- **WSGI Server**: Gunicorn
- **Static Files**: WhiteNoise (no external web server needed)
- **Security**: Non-root user
- **Size**: ~193MB final image

## 🚀 Quick Start

### Build and Run

```bash
# Build the image
docker build -t my-django-app .

# Run in development mode
docker run -p 8000:8000 -e DEBUG=true my-django-app

# Run in production mode
docker run -p 8000:8000 -e DJANGO_SETTINGS_MODULE=app.settings_prod my-django-app
```

### Using Docker Compose

```bash
# Development with hot reload
docker-compose up web

# Production mode
docker-compose up web-prod

# Staging environment
docker-compose up web-staging
```

## 📁 Project Structure

```
my-app/
├── Dockerfile              # Multi-stage production build
├── docker-compose.yml      # Dev/staging/prod environments
├── .dockerignore           # Excludes unnecessary files
├── app/
│   ├── settings.py         # Development settings
│   └── settings_prod.py    # Production settings
└── staticfiles/            # Collected static files (created during build)
```

## 🔧 Environment Variables

### Development
- `DEBUG=true`
- `DJANGO_SETTINGS_MODULE=app.settings`

### Production
- `DEBUG=false`
- `DJANGO_SETTINGS_MODULE=app.settings_prod`
- `SECRET_KEY=your-secret-key`
- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- `DATABASE_URL=postgres://user:pass@host:port/db` (optional)

## 📦 Build Optimization

### Multi-stage Build
1. **Builder Stage**: Installs dependencies and builds the application
2. **Production Stage**: Copies only the virtual environment and application code

### Features
- Uses Alpine Linux for minimal size
- Leverages uv's virtual environment for clean dependency management
- WhiteNoise serves static files without nginx/apache
- Non-root user for security
- Optimized layer caching

## 🛡️ Security Features

- Non-root user (`appuser`)
- Minimal base image (Alpine)
- Production security headers
- Secure cookie settings in production
- No unnecessary packages in final image

## 📊 Performance

- **Image Size**: ~193MB
- **Build Time**: ~10 seconds (with cache)
- **Workers**: 2 Gunicorn workers by default
- **Memory**: Low memory footprint with Alpine

## 🔄 Development Workflow

### Local Development
```bash
# Build and run with volume mount for live reloading
docker-compose up web
```

### Testing Production Build
```bash
# Test production build locally
docker-compose up web-prod
```

### Deployment
```bash
# Build for production
docker build -t my-django-app:latest .

# Tag for registry
docker tag my-django-app:latest registry.example.com/my-django-app:latest

# Push to registry
docker push registry.example.com/my-django-app:latest
```

## 🗂️ Static Files

Static files are automatically collected during build:
- Django admin CSS/JS files
- Your application static files
- Compressed and optimized with WhiteNoise

## 🔍 Troubleshooting

### Common Issues

**Build fails at dependency installation:**
```bash
# Clear Docker cache and rebuild
docker system prune -a
docker build --no-cache -t my-django-app .
```

**Static files not loading:**
- Ensure `STATIC_ROOT` is set in settings
- Check that `collectstatic` runs during build
- Verify WhiteNoise middleware is installed

**Permission denied:**
- Make sure files are copied with correct ownership
- Check that `appuser` has necessary permissions

### Logs
```bash
# View container logs
docker logs <container-name>

# Follow logs in real-time
docker logs -f <container-name>
```

## 🚀 Production Deployment

### Environment Setup
1. Set production environment variables
2. Use proper secret key
3. Configure allowed hosts
4. Set up database (if using external DB)
5. Configure SSL/TLS termination (load balancer/reverse proxy)

### Recommended Production Stack
- **Container Orchestration**: Kubernetes or Docker Swarm
- **Load Balancer**: nginx or cloud load balancer
- **Database**: PostgreSQL (external)
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack or cloud logging

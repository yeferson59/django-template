# Django Application with Automated Code Quality

A modern Django web application with automated code quality checks, Docker optimization, and comprehensive development tools.

## 🚀 Features

- **Django 5.2**: Latest Django framework with modern features
- **Docker Multi-stage Build**: Optimized production container (~308MB)
- **Automated Code Quality**: Pre-commit hooks with formatting, linting, and testing
- **Package Management**: UV for fast Python dependency management
- **Static Files**: WhiteNoise for efficient static file serving
- **Development Tools**: Complete setup with debugging, testing, and documentation
- **Production Ready**: Security headers, environment configurations, and deployment scripts

## 📦 Technology Stack

- **Framework**: Django 5.2.1
- **Python**: 3.13
- **Package Manager**: UV
- **WSGI Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Containerization**: Docker with Alpine Linux
- **Code Quality**: Black, isort, flake8, mypy, pytest
- **Git Hooks**: Pre-commit automation

## 🛠️ Development Tools

### Code Quality Automation
- **Black**: Code formatting with 88-character line length
- **isort**: Import sorting with Django-aware grouping
- **flake8**: PEP 8 compliance and error detection
- **mypy**: Type checking with Django stubs
- **pytest**: Testing framework with coverage reporting
- **pre-commit**: Automated quality checks on every commit

### Development Environment
- **Django Debug Toolbar**: SQL query analysis and performance monitoring
- **IPython**: Enhanced interactive shell
- **Django Extensions**: Additional management commands
- **Coverage Reports**: HTML and terminal coverage reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- UV package manager
- Docker (optional)
- Git

### Installation

1. **Clone and setup the project:**
```bash
git clone <repository-url>
cd my-app
./setup.sh
```

2. **Or manual setup:**
```bash
# Install dependencies
make install-dev

# Setup development environment
make dev-setup

# Start development server
make runserver
```

### Docker Development

```bash
# Development with hot reload
docker-compose up web

# Production testing
docker-compose up web-prod

# Full stack (web + database + redis)
docker-compose up
```

## 📋 Available Commands

### Development
```bash
make help              # Show all available commands
make install-dev       # Install development dependencies
make dev-setup         # Complete development environment setup
make runserver         # Start Django development server
make shell            # Open Django shell
make createsuperuser  # Create Django superuser
```

### Code Quality
```bash
make format           # Format code with Black and isort
make lint            # Run linting with flake8
make type-check      # Run type checking with mypy
make test            # Run tests with pytest
make test-cov        # Run tests with coverage report
make check           # Run all quality checks
```

### Database
```bash
make migrate          # Apply database migrations
make makemigrations   # Create new migrations
```

### Docker
```bash
make docker-build     # Build production Docker image
make docker-run       # Run Docker container
make docker-dev       # Start development environment
make docker-prod      # Start production environment
```

### Pre-commit Hooks
```bash
make pre-commit-install   # Install pre-commit hooks
make pre-commit-run      # Run hooks on all files
make pre-commit-update   # Update hook versions
```

## 🔧 Environment Configuration

### Development (.env)
```bash
DEBUG=true
DJANGO_SETTINGS_MODULE=app.settings
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Production
```bash
DEBUG=false
DJANGO_SETTINGS_MODULE=app.settings_prod
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 📁 Project Structure

```
my-app/
├── app/                     # Django application
│   ├── settings.py          # Development settings
│   ├── settings_prod.py     # Production settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_basic.py
├── staticfiles/             # Collected static files
├── .venv/                   # Virtual environment (UV)
├── pyproject.toml           # Dependencies and tool configuration
├── uv.lock                  # Locked dependencies
├── Dockerfile               # Production container
├── docker-compose.yml       # Multi-service development
├── Makefile                 # Development commands
├── .pre-commit-config.yaml  # Automated quality checks
├── .flake8                  # Linting configuration
├── .pylintrc                # Pylint configuration
├── pytest.ini              # Test configuration
├── setup.sh                 # Project setup script
├── .env.example             # Environment variables template
├── DEV.md                   # Development workflow guide
└── DOCKER.md                # Docker configuration guide
```

## 🔄 Development Workflow

### Making Changes
```bash
# 1. Make your changes
vim app/views.py

# 2. Add files to git
git add .

# 3. Commit (pre-commit hooks run automatically)
git commit -m "feat: add new feature"

# The pre-commit hooks will:
# - Format code with Black and isort
# - Check code quality with flake8
# - Run type checking with mypy
# - Execute fast tests with pytest
# - Validate Django configuration
```

### Automated Quality Checks
Every commit automatically runs:
- **Code Formatting**: Black + isort
- **Linting**: flake8 with PEP 8 compliance
- **Type Checking**: mypy with Django stubs
- **Testing**: pytest with coverage
- **Django Validation**: System checks and migration validation
- **File Cleanup**: Trailing whitespace, end-of-file fixes

## 🐳 Docker Information

### Image Details
- **Base**: Alpine Linux (lightweight)
- **Size**: ~308MB (optimized multi-stage build)
- **Security**: Non-root user, minimal packages
- **Performance**: 2 Gunicorn workers, optimized caching

### Build Optimization
- Multi-stage build for minimal production image
- Layer caching for faster subsequent builds
- Comprehensive .dockerignore for build efficiency
- Separate development and production configurations

## 🛡️ Security Features

- **Security Headers**: HSTS, XSS protection, content type nosniff
- **Secure Cookies**: Production cookie security settings
- **Non-root User**: Docker container runs as non-privileged user
- **Minimal Attack Surface**: Alpine Linux with essential packages only
- **Environment Separation**: Distinct development and production settings

## 📊 Code Quality Standards

- **Test Coverage**: Minimum 50% (configurable)
- **Code Style**: Black formatting with 88-character lines
- **Import Organization**: isort with Django-aware grouping
- **Type Safety**: mypy type checking enabled
- **PEP 8 Compliance**: flake8 linting with sensible exceptions

## 🚀 Deployment

### Production Build
```bash
# Build optimized production image
make docker-build

# Test production build locally
make docker-prod

# Deploy to registry
docker tag my-django-app:latest your-registry/my-django-app:latest
docker push your-registry/my-django-app:latest
```

### Environment Variables
Set these in your production environment:
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (optional)
- `DJANGO_SETTINGS_MODULE`: `app.settings_prod`

## 🔍 Troubleshooting

### Common Issues

**Pre-commit hooks failing:**
```bash
# Run checks manually
make check

# Update hooks
make pre-commit-update
```

**Docker build issues:**
```bash
# Clean build cache
docker system prune -a
make docker-build
```

**Static files not loading:**
```bash
# Collect static files
make collectstatic
```

## 📚 Documentation

- [Development Workflow](DEV.md) - Detailed development guide
- [Docker Configuration](DOCKER.md) - Docker setup and deployment
- [Django Documentation](https://docs.djangoproject.com/)
- [UV Package Manager](https://github.com/astral-sh/uv)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Commit your changes (pre-commit hooks will run)
6. Push to your branch
7. Create a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- UV team for fast Python package management
- Pre-commit maintainers for code quality automation
- Alpine Linux for lightweight container images

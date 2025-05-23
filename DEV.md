# Django Development Workflow

## 🚀 Quick Start

### Initial Setup
```bash
# Clone and setup
git clone <your-repo>
cd my-app

# Install development dependencies
make install-dev

# Setup development environment
make dev-setup

# Start development server
make runserver
```

## 🛠️ Development Tools

### Package Management with UV
```bash
# Install production dependencies
uv sync

# Install with development dependencies
uv sync --group dev

# Add new dependency
uv add package-name

# Add development dependency
uv add --group dev package-name

# Update dependencies
uv sync --upgrade
```

### Code Quality Tools

#### Formatting
```bash
# Format all code with Black and isort
make format

# Or individually
uv run black .
uv run isort .
```

#### Linting
```bash
# Run all linters
make lint

# Individual tools
uv run flake8 .
uv run pylint app/
```

#### Type Checking
```bash
# Run mypy type checking
make type-check
```

#### Complete Quality Check
```bash
# Run format, lint, type-check, and test
make check
```

### Testing
```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
uv run pytest app/tests/test_models.py

# Run with verbose output
uv run pytest -v
```

## 🐳 Docker Development

### Development Environment
```bash
# Build and run development container
make docker-dev

# Or using docker-compose directly
docker-compose up web
```

### Production Testing
```bash
# Test production build locally
make docker-prod

# Build production image
make docker-build
```

### Full Stack Development
```bash
# Start all services (web, db, redis)
docker-compose up

# Start specific services
docker-compose up web db

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
├── app/                    # Django application
│   ├── settings.py         # Development settings
│   ├── settings_prod.py    # Production settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── staticfiles/            # Collected static files
├── .venv/                  # Virtual environment (created by uv)
├── pyproject.toml          # Dependencies and tool configuration
├── uv.lock                 # Locked dependencies
├── Dockerfile              # Production container
├── docker-compose.yml      # Multi-service development
├── Makefile               # Development commands
├── .flake8                # Linting configuration
├── .pylintrc              # Pylint configuration
└── .env.example           # Environment variables template
```

## 🔧 Django Management

### Database
```bash
# Create migrations
make makemigrations

# Apply migrations
make migrate

# Create superuser
make createsuperuser

# Open Django shell
make shell
```

### Static Files
```bash
# Collect static files
make collectstatic
```

### Development Server
```bash
# Run development server
make runserver

# Or with uv directly
uv run python manage.py runserver
```

## 📊 Code Quality Standards

### Formatting Rules
- **Black**: Line length 88 characters
- **isort**: Import sorting with Django-aware grouping
- **Consistent**: Double quotes, trailing commas

### Linting Rules
- **flake8**: PEP 8 compliance with exceptions for Black
- **pylint**: Code quality and Django best practices
- **mypy**: Type checking with Django stubs

### Test Coverage
- Minimum 80% coverage target
- Exclude migrations, settings, and test files
- HTML coverage reports in `htmlcov/`

## 🌍 Environment Configuration

### Development (.env)
```bash
DEBUG=true
DJANGO_SETTINGS_MODULE=app.settings
SECRET_KEY=your-dev-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production
```bash
DEBUG=false
DJANGO_SETTINGS_MODULE=app.settings_prod
SECRET_KEY=your-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🚀 Deployment Workflow

### 1. Code Quality Check
```bash
make check
```

### 2. Build Production Image
```bash
make docker-build
```

### 3. Test Production Build
```bash
make docker-prod
```

### 4. Deploy
```bash
# Tag for registry
docker tag my-django-app:latest registry.example.com/my-django-app:latest

# Push to registry
docker push registry.example.com/my-django-app:latest
```

## 🐛 Common Development Tasks

### Adding a New Django App
```bash
uv run python manage.py startapp myapp
# Add 'myapp' to INSTALLED_APPS in settings.py
```

### Database Reset
```bash
rm db.sqlite3
make migrate
make createsuperuser
```

### Dependency Updates
```bash
uv sync --upgrade
uv lock
```

### Clean Development Environment
```bash
make clean
```

## 📝 Git Workflow

### Pre-commit Checks
```bash
# Before committing, always run:
make check

# This runs:
# - Code formatting (black, isort)
# - Linting (flake8, pylint)
# - Type checking (mypy)
# - Tests (pytest)
```

### Recommended Commit Flow
```bash
# Make changes
git add .

# Run quality checks
make check

# Commit if all checks pass
git commit -m "feat: add new feature"

# Push
git push
```

## 🔍 Debugging

### Django Debug Toolbar (Development)
- Automatically enabled in development
- Available when DEBUG=True
- Shows SQL queries, cache usage, templates

### Container Debugging
```bash
# Enter running container
docker exec -it <container-name> /bin/sh

# View container logs
docker logs <container-name>

# Debug with development overrides
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
```

### Python Debugging
```bash
# Use Django shell
make shell

# IPython debugging
uv run ipython

# Run specific management command
uv run python manage.py <command>
```

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Black Code Formatter](https://black.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)

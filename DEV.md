# Django Development Workflow

## 🚀 Quick Start

### Initial Setup
```bash
# Clone and setup project
git clone <your-repo>
cd my-app

# Automated setup (recommended)
./setup.sh

# Manual setup
make install-dev
make dev-setup
make runserver
```

### First Steps After Setup
```bash
# Create superuser for Django admin
make createsuperuser

# Run development server
make runserver

# Access application
# http://localhost:8000 - Main application
# http://localhost:8000/admin - Django admin interface
```

## 🛠️ Development Tools & Dependencies

### Package Management with UV
```bash
# Install production dependencies only
uv sync

# Install with development dependencies
uv sync --group dev

# Add new production dependency
uv add package-name

# Add development dependency
uv add --group dev package-name

# Update all dependencies
uv sync --upgrade

# Lock dependencies
uv lock
```

### Development Dependencies (Included)
- **Code Quality**: black, isort, flake8, mypy, pre-commit
- **Testing**: pytest, pytest-django, pytest-cov, factory-boy
- **Development**: django-debug-toolbar, django-extensions, ipython
- **Type Checking**: mypy, django-stubs
- **Environment**: python-dotenv

### Production Dependencies
- **Framework**: django, gunicorn, whitenoise
- **Database**: psycopg2-binary, dj-database-url (optional)
- **Monitoring**: sentry-sdk[django] (optional)
- **Caching**: redis, django-redis (optional)

## 🔧 Automated Code Quality (Pre-commit Hooks)

### What Runs Automatically on Every Commit
✅ **Black**: Code formatting with 88-character lines
✅ **isort**: Import sorting with Django-aware grouping
✅ **flake8**: PEP 8 compliance and error detection
✅ **mypy**: Type checking with Django stubs
✅ **pytest**: Fast test execution
✅ **Django checks**: System validation and migration checks
✅ **File cleanup**: Trailing whitespace, end-of-file fixes

### Pre-commit Commands
```bash
# Install hooks (done automatically by setup.sh)
make pre-commit-install

# Run hooks on all files manually
make pre-commit-run

# Update hook versions
make pre-commit-update

# Clean pre-commit cache
make pre-commit-clean
```

### Manual Code Quality Commands
```bash
# Format code with Black and isort
make format

# Run linting (flake8)
make lint

# Run type checking (mypy)
make type-check

# Run all tests
make test

# Run tests with coverage report
make test-cov

# Run all quality checks
make check
```

## 🔄 Git Workflow with Automated Quality

### Standard Development Flow
```bash
# 1. Make your changes
vim app/views.py
vim tests/test_views.py

# 2. Add files to git staging
git add .

# 3. Commit (hooks run automatically)
git commit -m "feat: add user authentication"

# Pre-commit hooks automatically:
# - Format code with Black and isort
# - Check code quality with flake8
# - Run type checking with mypy
# - Execute fast tests
# - Validate Django configuration
# - Fix file formatting issues

# 4. Push when hooks pass
git push origin feature-branch
```

### If Pre-commit Hooks Fail
```bash
# Hooks will show what failed and fix what they can
# Review the changes and commit again
git add .
git commit -m "feat: add user authentication"

# For persistent issues, run manual checks
make check
```

## 🐳 Docker Development

### Development with Docker Compose
```bash
# Start development environment
make docker-dev
# or
docker-compose up web

# Full stack (web + database + redis)
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell

# Stop all services
docker-compose down
```

### Production Testing with Docker
```bash
# Test production build locally
make docker-prod
# or
docker-compose up web-prod

# Build production image
make docker-build

# Run production container
make docker-run
```

### Available Docker Services
- **web**: Django development server with hot reload
- **web-prod**: Production-like environment with Gunicorn
- **web-staging**: Staging environment configuration
- **db**: PostgreSQL database
- **redis**: Redis cache server

## 📁 Project Structure

```
my-app/
├── app/                        # Django application
│   ├── __init__.py
│   ├── settings.py             # Development settings
│   ├── settings_prod.py        # Production settings
│   ├── urls.py                 # URL configuration
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
├── tests/                      # Test suite
│   ├── __init__.py
│   └── test_basic.py          # Basic application tests
├── staticfiles/                # Collected static files (auto-generated)
├── .venv/                      # Virtual environment (UV managed)
├── pyproject.toml              # Dependencies and tool configuration
├── uv.lock                     # Locked dependencies
├── pytest.ini                 # Test configuration
├── Dockerfile                  # Production container
├── docker-compose.yml          # Multi-environment setup
├── Makefile                    # Development commands
├── setup.sh                    # Project setup script
├── .env.example               # Environment template
├── .pre-commit-config.yaml    # Automated quality checks
├── .flake8                    # Linting configuration
├── .pylintrc                  # Pylint configuration (simplified)
├── .gitignore                 # Git exclusions
├── .dockerignore              # Docker build exclusions
└── README.md                  # Project overview
```

## 🔧 Django Management Commands

### Database Operations
```bash
# Create and apply migrations
make makemigrations
make migrate

# Reset database (development only)
rm db.sqlite3
make migrate

# Create superuser
make createsuperuser

# Django shell with IPython
make shell
```

### Static Files
```bash
# Collect static files
make collectstatic

# Find static files
uv run python manage.py findstatic admin/css/base.css
```

### Development Server
```bash
# Run development server
make runserver

# Run with specific settings
uv run python manage.py runserver --settings=app.settings_prod

# Run on different port
uv run python manage.py runserver 0.0.0.0:9000
```

## 🧪 Testing Framework

### Running Tests
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
uv run pytest tests/test_basic.py

# Run with verbose output
uv run pytest -v

# Run and stop on first failure
uv run pytest -x

# Run tests matching pattern
uv run pytest -k "test_user"
```

### Test Configuration
- **Framework**: pytest with pytest-django
- **Coverage**: Minimum 50% (configurable in pytest.ini)
- **Location**: Tests in `tests/` directory
- **Database**: Separate test database created automatically
- **Fixtures**: Factory Boy for test data generation

### Writing Tests
```python
# Example test structure
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestUserAuthentication(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_login(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(response)
```

## 🌍 Environment Configuration

### Development Environment (.env)
```bash
DEBUG=true
DJANGO_SETTINGS_MODULE=app.settings
SECRET_KEY=dev-secret-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_DEBUG_TOOLBAR=true
```

### Production Environment
```bash
DEBUG=false
DJANGO_SETTINGS_MODULE=app.settings_prod
SECRET_KEY=your-secure-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database Configuration (Optional)
```bash
# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=mydatabase
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432

# Or use DATABASE_URL
DATABASE_URL=postgres://user:password@host:port/database
```

## 📊 Code Quality Standards

### Formatting Standards
- **Line Length**: 88 characters (Black default)
- **Quotes**: Double quotes preferred
- **Import Sorting**: Django-aware grouping with isort
- **Trailing Commas**: Enforced for multi-line structures

### Linting Rules
- **PEP 8**: Enforced with reasonable exceptions
- **Django Best Practices**: Configured for Django projects
- **Type Hints**: Encouraged and checked with mypy
- **Security**: Basic security checks included

### Test Coverage Requirements
- **Minimum Coverage**: 50% (adjustable in pytest.ini)
- **Excluded Files**: Migrations, settings, venv directories
- **Coverage Reports**: HTML and terminal output
- **Location**: Coverage reports in `htmlcov/` directory

## 🚀 Production Deployment Workflow

### Pre-deployment Checklist
```bash
# 1. Run all quality checks
make check

# 2. Ensure tests pass
make test-cov

# 3. Build production image
make docker-build

# 4. Test production build locally
make docker-prod

# 5. Verify static files and admin access
curl http://localhost:8001/admin/
curl http://localhost:8001/static/admin/css/base.css
```

### Deployment Commands
```bash
# Build and tag for registry
docker build -t my-django-app:latest .
docker tag my-django-app:latest registry.example.com/my-django-app:latest

# Push to registry
docker push registry.example.com/my-django-app:latest

# Deploy to production environment
# (depends on your deployment platform)
```

## 🐛 Common Development Tasks

### Adding New Django App
```bash
# Create new app
uv run python manage.py startapp myapp

# Add to INSTALLED_APPS in settings.py
# Create initial tests in tests/test_myapp.py
# Add URL patterns if needed
```

### Dependency Management
```bash
# Add new package
uv add requests

# Add development package
uv add --group dev pytest-mock

# Update specific package
uv add django@5.2.2

# Remove package
uv remove package-name

# Sync after changes
uv sync
```

### Database Schema Changes
```bash
# Create migration
make makemigrations

# Apply migration
make migrate

# Show migration status
uv run python manage.py showmigrations

# Reverse migration (careful!)
uv run python manage.py migrate myapp 0001
```

### Debugging and Development
```bash
# Django shell with IPython
make shell

# Run Django shell in container
docker-compose exec web python manage.py shell

# Debug with print statements
# Use Django's built-in logging
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Use Django Debug Toolbar (development only)
# Automatically available at http://localhost:8000
```

## 🔍 Troubleshooting

### Common Issues

**Pre-commit hooks failing:**
```bash
# Run manual checks to see specific issues
make check

# Update pre-commit hooks
make pre-commit-update

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "emergency fix"
```

**Dependency conflicts:**
```bash
# Clear virtual environment and reinstall
rm -rf .venv
uv sync --group dev
```

**Docker build issues:**
```bash
# Clean Docker cache
docker system prune -a
make docker-build
```

**Database issues:**
```bash
# Reset database (development)
rm db.sqlite3
make migrate

# Check database status
uv run python manage.py check --database default
```

**Static files not loading:**
```bash
# Collect static files
make collectstatic

# Verify WhiteNoise configuration
uv run python manage.py findstatic admin/css/base.css
```

### Performance Debugging

**Slow tests:**
```bash
# Run with timing
uv run pytest --durations=10

# Run specific slow tests
uv run pytest -m slow
```

**Memory usage:**
```bash
# Monitor in development
pip install memory-profiler
# Add @profile decorator to functions
```

## 📚 Development Resources

### Documentation
- [Django 5.2 Documentation](https://docs.djangoproject.com/en/5.2/)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Pre-commit Framework](https://pre-commit.com/)

### Useful Django Packages
- **django-extensions**: Enhanced management commands
- **django-debug-toolbar**: Development debugging
- **factory-boy**: Test data generation
- **django-environ**: Environment variable management
- **django-cors-headers**: CORS handling for APIs

### Code Quality Tools
- **Black**: Uncompromising code formatter
- **isort**: Import statement organizer
- **flake8**: Linting and style checking
- **mypy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Git hook management

## 🤝 Contributing Guidelines

### Code Style
- Follow PEP 8 (enforced by flake8)
- Use Black formatting (enforced by pre-commit)
- Add type hints where possible
- Write docstrings for public functions
- Keep functions small and focused

### Testing Requirements
- Write tests for new features
- Maintain or improve test coverage
- Use descriptive test names
- Test both success and failure cases
- Use factories for test data

### Git Commit Messages
```bash
# Format: type(scope): description
feat(auth): add user registration endpoint
fix(models): resolve user profile cascade deletion
docs(readme): update installation instructions
test(views): add authentication test cases
refactor(utils): simplify email validation logic
```

### Pull Request Process
1. Create feature branch from main
2. Implement changes with tests
3. Ensure all pre-commit checks pass
4. Run full test suite: `make test-cov`
5. Update documentation if needed
6. Submit pull request with clear description

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-21

### Added
- Complete test suite with 91% coverage (42 tests)
- Security checking with Bandit integration
- New test files:
  - `tests/test_asgi_wsgi.py` - ASGI/WSGI configuration tests
  - `tests/test_management_commands.py` - Django management command tests
  - `tests/test_settings.py` - Django settings configuration tests
- Enhanced `tests/test_basic.py` with views, context processors, and URL tests
- Bandit configuration in pyproject.toml
- Type annotations for better mypy compatibility

### Updated
- **Django**: 5.2.1 → 5.2.3
- **Gunicorn**: 22.0.0 → 23.0.0
- **Whitenoise**: 6.6.0 → 6.9.0
- **Black**: 24.0.0 → 25.1.0
- **isort**: 5.13.0 → 6.0.1
- **Flake8**: 7.0.0 → 7.3.0
- **Pylint**: 3.0.0 → 3.3.10
- **MyPy**: 1.8.0 → 1.14.1
- **Django-stubs**: 4.2.0 → 5.2.1
- **Pytest**: 8.0.0 → 8.4.1
- **Pytest-Django**: 4.8.0 → 4.11.1
- **Pytest-cov**: 4.0.0 → 6.2.1
- **Factory-boy**: 3.3.0 → 3.3.3
- **Django-debug-toolbar**: 4.2.0 → 5.2.0
- **Django-extensions**: 3.2.0 → 4.1.0
- **IPython**: 8.20.0 → 8.31.0
- **Python-dotenv**: 1.0.0 → 1.0.1
- **Pre-commit**: 3.6.0 → 4.0.1
- **Psycopg2-binary**: 2.9.9 → 2.9.10
- **dj-database-url**: 2.1.0 → 2.3.0
- **Sentry-sdk[django]**: 1.40.0 → 2.20.0
- **Redis**: 5.0.0 → 5.2.1

### Changed
- Enhanced Makefile with Bandit integration
- Updated pre-commit hooks to latest versions
- Improved test coverage from 40% to 91%
- Enhanced pre-commit configuration with security checks
- Updated requirements files with exact versions
- Fixed security warning for hardcoded password in development command

### Fixed
- MyPy type checking errors in test files
- Bandit security warnings
- Pre-commit hook configurations
- Test failures and improved test reliability

## [0.1.0] - 2025-06-20

### Added
- Initial Django project template
- Complete project structure with apps/, templates/, static/, media/, logs/ directories
- Docker and Docker Compose configuration
- GitHub Actions CI/CD workflow
- Comprehensive Makefile with development commands
- Pre-commit hooks configuration
- Django settings for development and production
- Custom management command for project setup
- Basic HTML templates and CSS styling
- Environment variable configuration
- Logging configuration
- Cache configuration
- Security middleware setup

### Dependencies
- Django 5.2.1
- Gunicorn 22.0.0
- Whitenoise 6.6.0
- Development tools (Black, isort, flake8, pylint, mypy)
- Testing tools (pytest, pytest-django, pytest-cov)
- Development utilities (debug-toolbar, extensions, ipython)

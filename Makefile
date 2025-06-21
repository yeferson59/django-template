.PHONY: help install install-dev format lint test clean docker-build docker-run docker-dev init-project create-app

# Colors for pretty output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

# Default target
help:
	@echo "$(BLUE)🚀 Django Template - Available Commands$(NC)"
	@echo "$(BLUE)======================================$(NC)"
	@echo ""
	@echo "$(GREEN)📦 Dependencies:$(NC)"
	@echo "  install         Install production dependencies"
	@echo "  install-dev     Install development dependencies"
	@echo ""
	@echo "$(GREEN)🛠️  Development:$(NC)"
	@echo "  runserver       Start Django development server"
	@echo "  shell           Open Django shell"
	@echo "  createsuperuser Create Django superuser"
	@echo "  create-app      Create new Django app"
	@echo ""
	@echo "$(GREEN)🔧 Code Quality:$(NC)"
	@echo "  format          Format code with black and isort"
	@echo "  lint            Run linting with flake8 and pylint"
	@echo "  type-check      Run type checking with mypy"
	@echo "  test            Run tests with pytest"
	@echo "  test-cov        Run tests with coverage report"
	@echo "  check           Run all quality checks"
	@echo ""
	@echo "$(GREEN)🗄️  Database:$(NC)"
	@echo "  migrate         Run Django migrations"
	@echo "  makemigrations  Create new migrations"
	@echo "  reset-db        Reset database (development only)"
	@echo ""
	@echo "$(GREEN)📁 Static Files:$(NC)"
	@echo "  collectstatic   Collect static files"
	@echo ""
	@echo "$(GREEN)🐳 Docker:$(NC)"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-run      Run Docker container"
	@echo "  docker-dev      Run development environment with Docker Compose"
	@echo "  docker-prod     Run production environment with Docker Compose"
	@echo "  docker-stop     Stop Docker containers"
	@echo ""
	@echo "$(GREEN)🔗 Pre-commit:$(NC)"
	@echo "  pre-commit-install  Install pre-commit hooks"
	@echo "  pre-commit-run      Run pre-commit on all files"
	@echo "  pre-commit-update   Update pre-commit hooks"
	@echo ""
	@echo "$(GREEN)🎯 Setup:$(NC)"
	@echo "  init-project    Initialize new project from template"
	@echo "  dev-setup       Setup development environment"
	@echo "  prod-setup      Setup production environment"
	@echo "  clean           Clean cache and build files"

# Dependencies
install:
	uv sync --group prod

install-dev:
	uv sync --group dev

# Code formatting
format:
	uv run black .
	uv run isort .

# Linting
lint:
	uv run flake8 .
	uv run pylint app/
	uv run bandit -r app/

# Type checking
type-check:
	uv run mypy .

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov=app --cov-report=html --cov-report=term-missing

# Django commands
migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

collectstatic:
	uv run python manage.py collectstatic --noinput

createsuperuser:
	uv run python manage.py createsuperuser

runserver:
	uv run python manage.py runserver

shell:
	uv run python manage.py shell

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# Docker commands
docker-build:
	docker build -t my-django-app .

docker-run:
	docker run --rm -p 8000:8000 my-django-app

docker-dev:
	docker-compose up web

docker-prod:
	docker-compose up web-prod

docker-stop:
	docker-compose down

# Development workflow
check: format lint type-check test

dev-setup: install-dev migrate pre-commit-install
	@echo "$(GREEN)✅ Development environment ready!$(NC)"
	@echo "$(GREEN)🔗 Pre-commit hooks installed!$(NC)"
	@echo "$(BLUE)ℹ️  Static files will be served directly in development$(NC)"

prod-setup: install migrate collectstatic
	@echo "$(GREEN)✅ Production environment ready!$(NC)"

# Pre-commit hooks
pre-commit-install:
	uv run pre-commit install

pre-commit-run:
	uv run pre-commit run --all-files

pre-commit-update:
	uv run pre-commit autoupdate

pre-commit-clean:
	uv run pre-commit clean

# Project initialization
init-project:
	@echo "$(YELLOW)🚀 Initializing new project from template...$(NC)"
	./init_project.py

# Create new Django app
create-app:
	@echo "$(YELLOW)📱 Creating new Django app...$(NC)"
	@read -p "Enter app name: " app_name; \
	uv run python manage.py startapp $$app_name apps/$$app_name
	@echo "$(GREEN)✅ App created! Remember to add it to INSTALLED_APPS$(NC)"

# Reset database (development only)
reset-db:
	@echo "$(RED)⚠️  WARNING: This will delete your database!$(NC)"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		rm -f db.sqlite3; \
		uv run python manage.py migrate; \
		echo "$(GREEN)✅ Database reset complete!$(NC)"; \
	else \
		echo "$(YELLOW)❌ Database reset cancelled.$(NC)"; \
	fi

# Show logs
logs:
	tail -f logs/django.log

# Show Django version info
info:
	@echo "$(BLUE)📋 Project Information$(NC)"
	@echo "Django version: $$(uv run python -c 'import django; print(django.get_version())')"
	@echo "Python version: $$(python --version)"
	@echo "UV version: $$(uv --version)"
	@echo "Project root: $$(pwd)"

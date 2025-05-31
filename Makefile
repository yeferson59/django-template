.PHONY: help install install-dev format lint test clean docker-build docker-run docker-dev startapp

# Default target
help:
	@echo "Available commands:"
	@echo "  install         Install production dependencies"
	@echo "  install-dev     Install development dependencies"
	@echo "  format          Format code with black and isort"
	@echo "  lint            Run linting with flake8 and pylint"
	@echo "  type-check      Run type checking with mypy"
	@echo "  test            Run tests with pytest"
	@echo "  test-cov        Run tests with coverage report"
	@echo "  clean           Clean cache and build files"
	@echo "  migrate         Run Django migrations"
	@echo "  makemigrations  Create new Django migrations"
	@echo "  collectstatic   Collect static files"
	@echo "  createsuperuser Create a Django superuser"
	@echo "  runserver       Run the Django development server"
	@echo "  shell           Open a Django shell"
	@echo "  startapp        Create a new Django app (e.g., make startapp APP_NAME=my_app)"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-run      Run Docker container"
	@echo "  docker-dev      Run development environment with Docker Compose"
	@echo "  docker-prod     Run production environment with Docker Compose"
	@echo "  docker-stop     Stop Docker Compose services"
	@echo "  pre-commit-install  Install pre-commit hooks"
	@echo "  pre-commit-run      Run pre-commit on all files"
	@echo "  pre-commit-update   Update pre-commit hooks"
	@echo "  pre-commit-clean    Clean pre-commit cache"
	@echo "  check           Run format, lint, type-check, and test"
	@echo "  dev-setup       Setup development environment"
	@echo "  prod-setup      Setup production environment"


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

startapp:
	@if [ -z "$(APP_NAME)" ]; then \
		echo "Usage: make startapp APP_NAME=<app_name>"; \
		exit 1; \
	fi
	uv run python manage.py startapp $(APP_NAME)

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

dev-setup: install-dev migrate collectstatic pre-commit-install
	@echo "Development environment ready!"
	@echo "Pre-commit hooks installed!"

prod-setup: install migrate collectstatic
	@echo "Production environment ready!"

# Pre-commit hooks
pre-commit-install:
	uv run pre-commit install

pre-commit-run:
	uv run pre-commit run --all-files

pre-commit-update:
	uv run pre-commit autoupdate

pre-commit-clean:
	uv run pre-commit clean

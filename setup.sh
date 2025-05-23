#!/bin/bash

# Django Project Setup Script
# This script sets up the development environment with all necessary tools

set -e

echo "🚀 Setting up Django development environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install development dependencies
echo "📦 Installing development dependencies..."
uv sync --group dev

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
uv run pre-commit install

# Setup Django
echo "🗄️  Setting up Django database..."
uv run python manage.py migrate

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✏️  Please edit .env file with your settings"
fi

# Collect static files
echo "📁 Collecting static files..."
uv run python manage.py collectstatic --noinput

# Run initial code quality checks
echo "🔍 Running initial code quality checks..."
uv run pre-commit run --all-files || echo "⚠️  Some checks failed - please fix them before committing"

# Create superuser prompt
echo ""
echo "🎉 Setup complete!"
echo ""
echo "To create a Django superuser, run:"
echo "  make createsuperuser"
echo ""
echo "To start the development server, run:"
echo "  make runserver"
echo ""
echo "Pre-commit hooks are now active! They will run automatically on every commit."
echo ""
echo "Available commands:"
echo "  make help              - Show all available commands"
echo "  make format            - Format code"
echo "  make lint              - Run linting"
echo "  make test              - Run tests"
echo "  make check             - Run all quality checks"
echo "  make docker-dev        - Start with Docker"
echo ""

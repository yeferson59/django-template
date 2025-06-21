# My App

template for construction an app since beginnig

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- UV package manager
- Docker (optional)
- Git

### Installation

1. **Clone and setup the project:**
```bash
git clone <your-repository-url>
cd my-app
./setup.sh
```

2. **Create superuser:**
```bash
make createsuperuser
```

3. **Start development server:**
```bash
make runserver
```

### Access the application
- **Main application**: http://localhost:8000
- **Django admin**: http://localhost:8000/admin

## 🛠️ Development

### Quality Tools

- **Black**: Code formatting (v25.1.0)
- **isort**: Import sorting (v6.0.1)
- **flake8**: Linting (v7.3.0)
- **pylint**: Code analysis (v3.3.10)
- **mypy**: Type checking (v1.14.1)
- **bandit**: Security analysis (v1.8.5)
- **pytest**: Testing framework (v8.4.1)
- **pre-commit**: Git hooks (v4.0.1)

### Available Commands
```bash
make help              # Show all available commands
make install-dev       # Install development dependencies
make runserver         # Start development server
make test             # Run tests
make format           # Format code
make lint             # Run linting (includes security check)
make check            # Run all quality checks
make pre-commit-run    # Run pre-commit hooks
```

### Docker Development
```bash
# Development environment
make docker-dev

# Production testing
make docker-prod
```

## 📁 Project Structure

```
my-app/
├── app/                     # Django application
├── apps/                    # Custom Django apps
├── tests/                   # Test suite
├── static/                  # Static files
├── templates/               # HTML templates
├── requirements/            # Dependencies by environment
├── docker-compose.yml       # Docker services
├── Dockerfile              # Production container
└── Makefile               # Development commands
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Commit your changes
6. Push to your branch
7. Create a pull request

## 📄 License

This project is licensed under the MIT License.

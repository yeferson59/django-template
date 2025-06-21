#!/usr/bin/env python3
"""
Django Template Project Initializer
===================================

This script helps you initialize a new Django project from this template.
It will:
- Rename the project
- Update configuration files
- Set up environment variables
- Initialize git repository
- Create initial superuser
"""

import os
import re
import shutil
import subprocess  # nosec
import sys
from pathlib import Path


class ProjectInitializer:
    def __init__(self):
        self.template_dir = Path(__file__).parent
        self.project_name = None
        self.project_description = None
        self.author_name = None
        self.author_email = None

    def get_user_input(self):
        """Get project information from user."""
        print("🚀 Django Template Project Initializer")
        print("=" * 50)

        self.project_name = input("Enter project name (e.g., my-awesome-app): ").strip()
        if not self.project_name:
            print("❌ Project name is required!")
            sys.exit(1)

        self.project_description = input("Enter project description: ").strip()
        if not self.project_description:
            self.project_description = f"A Django application: {self.project_name}"

        self.author_name = input("Enter author name: ").strip()
        self.author_email = input("Enter author email: ").strip()

        print("\n📋 Project Configuration:")
        print(f"   Name: {self.project_name}")
        print(f"   Description: {self.project_description}")
        print(f"   Author: {self.author_name} <{self.author_email}>")

        confirm = input("\nProceed with initialization? (y/N): ").lower()
        if confirm != "y":
            print("❌ Initialization cancelled.")
            sys.exit(0)

    def update_pyproject_toml(self):
        """Update pyproject.toml with project information."""
        pyproject_path = self.template_dir / "pyproject.toml"

        with open(pyproject_path, "r") as f:
            content = f.read()

        # Update project information
        content = re.sub(r'name = ".*"', f'name = "{self.project_name}"', content)
        content = re.sub(
            r'description = ".*"',
            f'description = "{self.project_description}"',
            content,
        )

        if self.author_name:
            # Add authors section if not exists
            if "authors = [" not in content:
                authors_line = f'authors = [{{"name" = "{self.author_name}"'
                if self.author_email:
                    authors_line += f', "email" = "{self.author_email}"'
                authors_line += "}]\n"

                # Insert after description
                content = re.sub(
                    r'(description = ".*"\n)', f"\\1{authors_line}", content
                )

        with open(pyproject_path, "w") as f:
            f.write(content)

        print("✅ Updated pyproject.toml")

    def update_env_example(self):
        """Update .env.example with project-specific settings."""
        env_path = self.template_dir / ".env.example"

        with open(env_path, "r") as f:
            content = f.read()

        # Add project-specific variables
        project_vars = f"""
# Project Configuration
PROJECT_NAME={self.project_name}
PROJECT_DESCRIPTION="{self.project_description}"

"""
        content = project_vars + content

        with open(env_path, "w") as f:
            f.write(content)

        print("✅ Updated .env.example")

    def update_docker_compose(self):
        """Update docker-compose.yml with project name."""
        compose_path = self.template_dir / "docker-compose.yml"

        with open(compose_path, "r") as f:
            content = f.read()

        # Replace container names and image names
        content = re.sub(
            r"container_name: .*", f"container_name: {self.project_name}-web", content
        )
        content = re.sub(
            r"image: my-django-app", f"image: {self.project_name}", content
        )

        with open(compose_path, "w") as f:
            f.write(content)

        print("✅ Updated docker-compose.yml")

    def update_dockerfile(self):
        """Update Dockerfile with project name."""
        dockerfile_path = self.template_dir / "Dockerfile"

        with open(dockerfile_path, "r") as f:
            content = f.read()

        # Update labels
        content = re.sub(
            r'LABEL maintainer=".*"',
            (
                f'LABEL maintainer="{self.author_email}"'
                if self.author_email
                else 'LABEL maintainer="developer@example.com"'
            ),
            content,
        )

        with open(dockerfile_path, "w") as f:
            f.write(content)

        print("✅ Updated Dockerfile")

    def create_project_readme(self):
        """Create a project-specific README."""
        readme_path = self.template_dir / "README.md"

        project_title = (self.project_name or "Project").title().replace("-", " ")
        readme_content = f"""# {project_title}

{self.project_description}

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
cd {self.project_name}
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

### Available Commands
```bash
make help              # Show all available commands
make install-dev       # Install development dependencies
make runserver         # Start development server
make test             # Run tests
make format           # Format code
make lint             # Run linting
make check            # Run all quality checks
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
{self.project_name}/
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
"""

        with open(readme_path, "w") as f:
            f.write(readme_content)

        print("✅ Created project-specific README.md")

    def create_apps_directory(self):
        """Create apps directory structure for custom Django apps."""
        apps_dir = self.template_dir / "apps"
        apps_dir.mkdir(exist_ok=True)

        # Create __init__.py
        (apps_dir / "__init__.py").touch()

        print("✅ Created apps/ directory for custom Django apps")

    def create_additional_directories(self):
        """Create additional project directories."""
        directories = [
            "static",
            "static/css",
            "static/js",
            "static/images",
            "templates",
            "templates/base",
            "media",
            "logs",
            "requirements",
        ]

        for dir_path in directories:
            dir_full_path = self.template_dir / dir_path
            dir_full_path.mkdir(parents=True, exist_ok=True)

            # Create .gitkeep for empty directories
            if dir_path in [
                "static/css",
                "static/js",
                "static/images",
                "media",
                "logs",
            ]:
                (dir_full_path / ".gitkeep").touch()

        print("✅ Created additional project directories")

    def create_requirements_files(self):
        """Create requirements files for different environments."""
        requirements_dir = self.template_dir / "requirements"

        # Base requirements
        base_req = """# Base requirements
django>=5.2.1
gunicorn>=22.0.0
whitenoise>=6.6.0
python-dotenv>=1.0.0
"""

        # Development requirements
        dev_req = """-r base.txt

# Development tools
django-debug-toolbar>=4.2.0
django-extensions>=3.2.0
ipython>=8.20.0

# Code quality
black>=24.0.0
isort>=5.13.0
flake8>=7.0.0
mypy>=1.8.0
django-stubs>=4.2.0

# Testing
pytest>=8.0.0
pytest-django>=4.8.0
pytest-cov>=4.0.0
factory-boy>=3.3.0

# Pre-commit
pre-commit>=3.6.0
"""

        # Production requirements
        prod_req = """-r base.txt

# Database
psycopg2-binary>=2.9.9
dj-database-url>=2.1.0

# Monitoring
sentry-sdk[django]>=1.40.0

# Performance
redis>=5.0.0
django-redis>=5.4.0

# Security
django-cors-headers>=4.3.0
"""

        (requirements_dir / "base.txt").write_text(base_req)
        (requirements_dir / "development.txt").write_text(dev_req)
        (requirements_dir / "production.txt").write_text(prod_req)

        print("✅ Created requirements files")

    def update_settings(self):
        """Update Django settings for better project structure."""
        settings_path = self.template_dir / "app" / "settings.py"

        # Read current settings
        with open(settings_path, "r") as f:
            content = f.read()

        # Add project-specific configurations
        additions = f"""
import os
from pathlib import Path

# Project information
PROJECT_NAME = os.getenv('PROJECT_NAME', '{self.project_name}')
PROJECT_DESCRIPTION = os.getenv('PROJECT_DESCRIPTION', '{self.project_description}')

# Apps directory
APPS_DIR = BASE_DIR / 'apps'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates directory
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Add apps directory to Python path
import sys
sys.path.insert(0, str(APPS_DIR))
"""

        # Insert after BASE_DIR definition
        content = re.sub(
            r"(BASE_DIR = Path.*?\n)", f"\\1{additions}\n", content, flags=re.DOTALL
        )

        with open(settings_path, "w") as f:
            f.write(content)

        print("✅ Updated Django settings")

    def create_base_templates(self):
        """Create base HTML templates."""
        templates_dir = self.template_dir / "templates"
        base_dir = templates_dir / "base"
        project_title = (self.project_name or "Project").title().replace("-", " ")

        # Base HTML template
        base_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% block title %}}{project_title}{{% endblock %}}</title>

    {{% load static %}}
    <link rel="stylesheet" href="{{% static 'css/main.css' %}}">

    {{% block extra_css %}}{{% endblock %}}
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">{project_title}</a>
            </div>
        </nav>
    </header>

    <main>
        {{% block content %}}
        <div class="container">
            <h1>Welcome to {project_title}</h1>
            <p>{self.project_description}</p>
        </div>
        {{% endblock %}}
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 {project_title}. All rights reserved.</p>
        </div>
    </footer>

    <script src="{{% static 'js/main.js' %}}"></script>
    {{% block extra_js %}}{{% endblock %}}
</body>
</html>"""

        (base_dir / "base.html").write_text(base_html)

        # Home page template
        home_html = """{{% extends "base/base.html" %}}

{{% block title %}}Home - {{ block.super }}{{% endblock %}}

{{% block content %}}
<div class="container">
    <div class="hero">
        <h1>Welcome to {{ PROJECT_NAME|title }}</h1>
        <p class="lead">{{ PROJECT_DESCRIPTION }}</p>
        <a href="/admin/" class="btn btn-primary">Go to Admin</a>
    </div>
</div>
{{% endblock %}}"""

        (templates_dir / "home.html").write_text(home_html)

        print("✅ Created base HTML templates")

    def create_static_files(self):
        """Create basic static files."""
        static_dir = self.template_dir / "static"

        # Main CSS
        main_css = """/* Main Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
}

.nav-brand a {
    color: white;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}

/* Main content */
main {
    flex: 1;
    padding: 2rem 0;
}

.hero {
    text-align: center;
    padding: 4rem 0;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

.lead {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    color: #6c757d;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    text-decoration: none;
    border-radius: 0.375rem;
    font-weight: 500;
    transition: all 0.15s ease;
}

.btn-primary {
    background: #007bff;
    color: white;
    border: 2px solid #007bff;
}

.btn-primary:hover {
    background: #0056b3;
    border-color: #0056b3;
}

/* Footer */
footer {
    background: #f8f9fa;
    border-top: 1px solid #dee2e6;
    padding: 2rem 0;
    text-align: center;
    color: #6c757d;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }

    .container {
        padding: 0 15px;
    }
}
"""

        (static_dir / "css" / "main.css").write_text(main_css)

        # Main JavaScript
        main_js = """// Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Project initialized successfully!');

    // Add any global JavaScript functionality here
});
"""

        (static_dir / "js" / "main.js").write_text(main_js)

        print("✅ Created basic static files")

    def run(self):
        """Run the complete initialization process."""
        try:
            self.get_user_input()

            print("\n🔧 Initializing project...")

            self.update_pyproject_toml()
            self.update_env_example()
            self.update_docker_compose()
            self.update_dockerfile()
            self.create_project_readme()
            self.create_apps_directory()
            self.create_additional_directories()
            self.create_requirements_files()
            self.update_settings()
            self.create_base_templates()
            self.create_static_files()

            print("\n✅ Project initialization completed!")
            print(f"\n🎉 Your project '{self.project_name}' is ready!")
            print("\n📋 Next steps:")
            print("1. Review and edit .env.example, then copy to .env")
            print("2. Run: ./setup.sh")
            print("3. Run: make createsuperuser")
            print("4. Run: make runserver")
            print("5. Visit: http://localhost:8000")

        except KeyboardInterrupt:
            print("\n❌ Initialization cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error during initialization: {e}")
            sys.exit(1)


if __name__ == "__main__":
    initializer = ProjectInitializer()
    initializer.run()

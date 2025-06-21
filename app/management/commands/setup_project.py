"""
Django management command to setup the project.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Setup the project with initial data and configuration"

    def add_arguments(self, parser):
        parser.add_argument(
            "--create-superuser",
            action="store_true",
            help="Create a superuser interactively",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Username for superuser (non-interactive)",
        )
        parser.add_argument(
            "--email",
            type=str,
            help="Email for superuser (non-interactive)",
        )

    def handle(self, *args, **options):
        self.stdout.write("🚀 Setting up Django project...")

        # Display project information
        self.stdout.write(f"Project: {settings.PROJECT_NAME}")
        self.stdout.write(f"Description: {settings.PROJECT_DESCRIPTION}")
        self.stdout.write(f"Debug mode: {settings.DEBUG}")

        # Create logs directory if it doesn't exist
        logs_dir = settings.BASE_DIR / "logs"
        logs_dir.mkdir(exist_ok=True)
        self.stdout.write("✅ Logs directory created")

        # Create media directory if it doesn't exist
        media_dir = settings.BASE_DIR / "media"
        media_dir.mkdir(exist_ok=True)
        self.stdout.write("✅ Media directory created")

        # Create superuser if requested
        if options["create_superuser"]:
            self.create_superuser(options)

        self.stdout.write("✅ Project setup completed!")

    @transaction.atomic
    def create_superuser(self, options):
        """Create a superuser."""
        User = get_user_model()

        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("⚠️  Superuser already exists. Skipping...")
            return

        if options["username"] and options["email"]:
            # Non-interactive mode
            username = options["username"]
            email = options["email"]
            password = "admin123"  # Default password for development  # nosec B105

            User.objects.create_superuser(
                username=username, email=email, password=password
            )

            self.stdout.write(f'✅ Superuser "{username}" created!')
            self.stdout.write(f"🔑 Default password: {password}")
        else:
            # Interactive mode
            self.stdout.write("Creating superuser interactively...")
            from django.core.management import call_command

            call_command("createsuperuser")

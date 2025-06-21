"""
Tests for Django management commands.
"""

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


class SetupProjectCommandTestCase(TestCase):
    """Test setup_project management command."""

    def test_setup_project_command_exists(self):
        """Test that setup_project command can be imported."""
        from app.management.commands.setup_project import Command

        self.assertIsNotNone(Command)
        self.assertTrue(hasattr(Command, "handle"))

    def test_setup_project_command_help(self):
        """Test that setup_project command has help text."""
        from app.management.commands.setup_project import Command

        command = Command()
        self.assertIsNotNone(command.help)
        self.assertIn("Setup the project", command.help)

    def test_setup_project_command_output(self):
        """Test setup_project command produces output."""
        out = StringIO()

        call_command("setup_project", stdout=out)
        output = out.getvalue()

        self.assertIn("Setting up Django project", output)

    def test_setup_project_superuser_creation_no_options(self):
        """Test superuser creation when no options provided."""
        from app.management.commands.setup_project import Command

        command = Command()
        options = {"username": None, "email": None}

        # This should not create a superuser when no username is provided
        with patch("django.contrib.auth.models.User.objects.filter") as mock_filter:
            mock_filter.return_value.exists.return_value = False

            with patch("django.core.management.call_command") as mock_call:
                command.create_superuser(options)
                mock_call.assert_called_once_with("createsuperuser")

    def test_setup_project_superuser_creation_with_options(self):
        """Test superuser creation with username and email options."""
        from app.management.commands.setup_project import Command

        command = Command()
        options = {"username": "admin", "email": "admin@example.com"}

        with patch(
            "django.contrib.auth.models.User.objects.create_superuser"
        ) as mock_create:
            with patch("django.contrib.auth.models.User.objects.filter") as mock_filter:
                # Mock that user doesn't exist
                mock_filter.return_value.exists.return_value = False

                command.create_superuser(options)

                mock_create.assert_called_once_with(
                    username="admin", email="admin@example.com", password="admin123"
                )

    def test_setup_project_superuser_already_exists(self):
        """Test superuser creation when user already exists."""
        from app.management.commands.setup_project import Command

        command = Command()
        options = {"username": "admin", "email": "admin@example.com"}

        with patch("django.contrib.auth.models.User.objects.filter") as mock_filter:
            # Mock that user already exists
            mock_filter.return_value.exists.return_value = True

            with patch(
                "django.contrib.auth.models.User.objects.create_superuser"
            ) as mock_create:
                command.create_superuser(options)
                mock_create.assert_not_called()

    def test_setup_project_command_with_create_superuser_flag(self):
        """Test setup_project command with --create-superuser flag."""
        out = StringIO()

        # Mock the create_superuser method to avoid actual user creation
        with patch(
            "app.management.commands.setup_project.Command.create_superuser"
        ) as mock_create:
            call_command(
                "setup_project",
                "--create-superuser",
                stdout=out,
            )

            # Verify that create_superuser was called
            mock_create.assert_called_once()

            # Check command output
            output = out.getvalue()
            self.assertIn("Setting up Django project", output)
            self.assertIn("Project setup completed", output)

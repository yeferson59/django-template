from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

import pytest


class BasicTestCase(TestCase):
    """Basic tests for Django application."""

    def setUp(self):
        """Set up test dependencies."""
        self.client = Client()

    def test_django_settings_configured(self):
        """Test that Django settings are properly configured."""
        from django.conf import settings

        self.assertTrue(settings.configured)
        self.assertIsNotNone(settings.SECRET_KEY)

    def test_admin_urls_accessible(self):
        """Test that admin URLs are accessible."""
        response = self.client.get("/admin/")
        # Should redirect to login or show admin page
        self.assertIn(response.status_code, [200, 302])

    def test_static_files_configured(self):
        """Test that static files are properly configured."""
        from django.conf import settings

        self.assertIsNotNone(settings.STATIC_URL)
        self.assertIsNotNone(settings.STATIC_ROOT)


@pytest.mark.django_db
class DatabaseTestCase(TestCase):
    """Test database functionality."""

    def test_user_creation(self):
        """Test that we can create users."""
        user_count_before = User.objects.count()
        User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        user_count_after = User.objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

    def test_user_authentication(self):
        """Test user authentication."""
        User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        authenticated = self.client.login(username="testuser", password="testpass123")
        self.assertTrue(authenticated)


class StaticFilesTestCase(TestCase):
    """Test static files functionality."""

    def test_static_files_serve(self):
        """Test that static files can be served."""
        from django.conf import settings
        from django.contrib.staticfiles import finders

        # Test that we can find admin CSS files
        admin_css = finders.find("admin/css/base.css")
        self.assertIsNotNone(admin_css)


def test_environment_variables():
    """Test environment variables are accessible."""
    import os

    from django.conf import settings

    # Basic environment test
    assert hasattr(settings, "DEBUG")
    assert hasattr(settings, "SECRET_KEY")
    assert hasattr(settings, "ALLOWED_HOSTS")


def test_installed_apps():
    """Test that required apps are installed."""
    from django.conf import settings

    required_apps = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    for app in required_apps:
        assert app in settings.INSTALLED_APPS


def test_middleware_configured():
    """Test that required middleware is configured."""
    from django.conf import settings

    required_middleware = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    for middleware in required_middleware:
        assert middleware in settings.MIDDLEWARE


class ViewsTestCase(TestCase):
    """Test views functionality."""

    def setUp(self):
        """Set up test dependencies."""
        self.client = Client()

    def test_home_view(self):
        """Test home view returns correct response."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to My-App")
        self.assertIn("page_title", response.context)
        self.assertEqual(response.context["page_title"], "Home")

    def test_home_view_template_used(self):
        """Test home view uses correct template."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ContextProcessorTestCase(TestCase):
    """Test context processors functionality."""

    def test_project_context_processor(self):
        """Test project context processor adds correct variables."""
        from django.test import RequestFactory

        from app.context_processors import project_context

        factory = RequestFactory()
        request = factory.get("/")

        context = project_context(request)

        self.assertIn("PROJECT_NAME", context)
        self.assertIn("PROJECT_DESCRIPTION", context)
        self.assertIn("DEBUG", context)
        self.assertIsInstance(context["DEBUG"], bool)

    def test_project_context_in_template(self):
        """Test that project context is available in templates."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        # Check that context processor variables are available
        self.assertIn("PROJECT_NAME", response.context)
        self.assertIn("PROJECT_DESCRIPTION", response.context)
        self.assertIn("DEBUG", response.context)


class URLsTestCase(TestCase):
    """Test URL configuration."""

    def test_home_url_resolves(self):
        """Test that home URL resolves correctly."""
        from django.urls import resolve

        from app.views import home

        resolver = resolve("/")
        self.assertEqual(resolver.func, home)
        self.assertEqual(resolver.url_name, "home")

    def test_admin_url_exists(self):
        """Test that admin URL exists."""
        response = self.client.get("/admin/")
        # Should redirect to login or show admin page
        self.assertIn(response.status_code, [200, 302])

    def test_media_urls_in_debug_mode(self):
        """Test that media URLs are configured in debug mode."""
        from django.conf import settings
        from django.urls import reverse

        # This test assumes DEBUG=True in test settings
        if settings.DEBUG:
            # Test that we can access the URL patterns
            from django.conf.urls import include
            from django.conf.urls.static import static

            self.assertTrue(hasattr(settings, "MEDIA_URL"))
            self.assertTrue(hasattr(settings, "MEDIA_ROOT"))
            self.assertTrue(hasattr(settings, "STATIC_URL"))
            self.assertTrue(hasattr(settings, "STATIC_ROOT"))

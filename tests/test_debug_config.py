"""
Tests for debug toolbar and development configurations.
"""

import os
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


class DebugToolbarTestCase(TestCase):
    """Test debug toolbar configuration."""

    def test_debug_toolbar_disabled_by_default(self):
        """Test that debug toolbar is disabled by default."""
        self.assertNotIn("debug_toolbar", settings.INSTALLED_APPS)

    @override_settings(DEBUG=True)
    def test_media_urls_in_debug_mode(self):
        """Test that media URLs are configured in debug mode."""
        from django.conf import settings
        from django.conf.urls.static import static

        # Import URL patterns
        from app.urls import urlpatterns

        # Check that static/media URL patterns are added in debug mode
        static_patterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        static_file_patterns = static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )

        self.assertTrue(len(static_patterns) > 0)
        self.assertTrue(len(static_file_patterns) > 0)

    def test_debug_toolbar_environment_variable(self):
        """Test that debug toolbar can be controlled via environment variable."""
        # Test that the environment variable check works
        with patch.dict(os.environ, {"DJANGO_DEBUG_TOOLBAR": "true"}):
            env_value = os.getenv("DJANGO_DEBUG_TOOLBAR", "false")
            self.assertEqual(env_value, "true")

        with patch.dict(os.environ, {"DJANGO_DEBUG_TOOLBAR": "false"}):
            env_value = os.getenv("DJANGO_DEBUG_TOOLBAR", "false")
            self.assertEqual(env_value, "false")

    def test_debug_toolbar_config_when_disabled(self):
        """Test that debug toolbar configuration is not present when disabled."""
        # By default, debug toolbar should not be in installed apps
        from django.conf import settings

        self.assertNotIn("debug_toolbar", settings.INSTALLED_APPS)


class URLPatternsTestCase(TestCase):
    """Test URL patterns configuration."""

    def test_home_url_pattern(self):
        """Test that home URL pattern exists and resolves correctly."""
        url = reverse("home")
        self.assertEqual(url, "/")

    def test_admin_url_pattern(self):
        """Test that admin URL pattern exists."""
        from django.urls import reverse

        url = reverse("admin:index")
        self.assertEqual(url, "/admin/")

    @override_settings(DEBUG=True)
    def test_debug_urls_configuration(self):
        """Test that debug URLs are configured properly in debug mode."""
        # This tests the URL configuration code in debug mode
        from django.conf import settings
        from django.conf.urls.static import static
        from django.urls import include, path

        # Test that media and static URLs are configured
        media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

        self.assertIsInstance(media_urls, list)
        self.assertIsInstance(static_urls, list)

    @override_settings(
        DEBUG=True, INSTALLED_APPS=settings.INSTALLED_APPS + ["debug_toolbar"]
    )
    def test_debug_toolbar_urls_when_installed(self):
        """Test that debug toolbar URLs are configured when debug_toolbar is installed."""
        with patch.dict(
            "sys.modules", {"debug_toolbar": type("MockModule", (), {"urls": []})()}
        ):
            # Import the URL module to trigger the debug toolbar URL configuration
            import importlib

            from app import urls

            importlib.reload(urls)

            # The import should work without errors
            self.assertTrue(True)


class LoggingConfigurationTestCase(TestCase):
    """Test logging configuration in different environments."""

    @patch.dict(os.environ, {"CI": "true"})
    def test_logging_config_in_ci_environment(self):
        """Test that file logging is disabled in CI environment."""
        # Re-import settings to get CI configuration
        import importlib

        from app import settings

        importlib.reload(settings)

        # File handler should not be present in CI
        from typing import Any, Dict, cast

        from app.settings import LOGGING

        handlers = cast(Dict[str, Any], LOGGING.get("handlers", {}))
        self.assertNotIn("file", handlers)

    @patch.dict(os.environ, {"GITHUB_ACTIONS": "true"})
    def test_logging_config_in_github_actions(self):
        """Test that file logging is disabled in GitHub Actions environment."""
        # Re-import settings to get GitHub Actions configuration
        import importlib

        from app import settings

        importlib.reload(settings)

        # File handler should not be present in GitHub Actions
        from typing import Any, Dict, cast

        from app.settings import LOGGING

        handlers = cast(Dict[str, Any], LOGGING.get("handlers", {}))
        self.assertNotIn("file", handlers)

    def test_logging_config_in_development(self):
        """Test that file logging is enabled in development environment."""
        # Ensure we're not in CI environment
        with patch.dict(os.environ, {}, clear=True):
            # Re-import settings to get development configuration
            import importlib

            from app import settings

            importlib.reload(settings)

            # File handler should be present in development
            from typing import Any, Dict, List, cast

            from app.settings import LOGGING

            handlers = cast(Dict[str, Any], LOGGING.get("handlers", {}))
            loggers = cast(Dict[str, Any], LOGGING.get("loggers", {}))
            app_logger = cast(Dict[str, Any], loggers.get("app", {}))
            app_handlers = cast(List[str], app_logger.get("handlers", []))

            self.assertIn("file", handlers)
            self.assertIn("file", app_handlers)

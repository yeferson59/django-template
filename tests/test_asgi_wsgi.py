"""
Tests for ASGI and WSGI configuration.
"""

from django.test import TestCase


class ASGITestCase(TestCase):
    """Test ASGI configuration."""

    def test_asgi_application_exists(self):
        """Test that ASGI application can be imported."""
        from app.asgi import application

        self.assertIsNotNone(application)

    def test_asgi_application_callable(self):
        """Test that ASGI application is callable."""
        from app.asgi import application

        self.assertTrue(callable(application))

    def test_asgi_module_has_required_attributes(self):
        """Test that ASGI module has required attributes."""
        import app.asgi

        self.assertTrue(hasattr(app.asgi, "application"))
        self.assertTrue(hasattr(app.asgi, "os"))


class WSGITestCase(TestCase):
    """Test WSGI configuration."""

    def test_wsgi_application_exists(self):
        """Test that WSGI application can be imported."""
        from app.wsgi import application

        self.assertIsNotNone(application)

    def test_wsgi_application_callable(self):
        """Test that WSGI application is callable."""
        from app.wsgi import application

        self.assertTrue(callable(application))

    def test_wsgi_module_has_required_attributes(self):
        """Test that WSGI module has required attributes."""
        import app.wsgi

        self.assertTrue(hasattr(app.wsgi, "application"))
        self.assertTrue(hasattr(app.wsgi, "os"))

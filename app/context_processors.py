"""
Context processors for the Django project.
"""

from django.conf import settings


def project_context(request):
    """
    Add project-related context variables to all templates.

    This makes PROJECT_NAME, PROJECT_DESCRIPTION, and other
    project settings available in all templates.
    """
    return {
        "PROJECT_NAME": getattr(settings, "PROJECT_NAME", "Django App"),
        "PROJECT_DESCRIPTION": getattr(
            settings, "PROJECT_DESCRIPTION", "A Django Application"
        ),
        "DEBUG": settings.DEBUG,
    }

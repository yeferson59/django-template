"""
Views for the main Django application.
"""

from django.shortcuts import render


def home(request):
    """
    Home page view.

    Renders the home template with project context.
    """
    context = {
        "page_title": "Home",
    }
    return render(request, "home.html", context)

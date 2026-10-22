"""Application configuration for django-analytical."""

from django.apps import AppConfig


class AnalyticalConfig(AppConfig):
    name = 'analytical'

    def ready(self):
        from analytical.templatetags import clicky  # noqa: F401

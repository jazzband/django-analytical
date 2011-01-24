"""
Context processors for django-analytical.
"""

from django.conf import settings


IMPORT_SETTINGS = [
    'ANALYTICAL_INTERNAL_IPS',
    'ANALYTICAL_SERVICES',
    'CHARTBEAT_USER_ID',
    'CLICKY_SITE_ID',
    'CRAZY_EGG_ACCOUNT_NUMBER',
    'GOOGLE_ANALYTICS_PROPERTY_ID',
    'KISS_INSIGHTS_ACCOUNT_NUMBER',
    'KISS_INSIGHTS_SITE_CODE',
    'KISS_METRICS_API_KEY',
    'MIXPANEL_TOKEN',
    'OPTIMIZELY_ACCOUNT_NUMBER',
]


def settings(request):
    """
    Import all django-analytical settings into the template context.
    """
    vars = {}
    for setting in IMPORT_SETTINGS:
        try:
            vars[setting] = getattr(settings, setting)
        except AttributeError:
            pass
    return vars

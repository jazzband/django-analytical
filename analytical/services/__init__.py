"""
Analytics services.
"""

import logging

from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured


_log = logging.getLogger(__name__)

DEFAULT_SERVICES = [
    'analytical.services.clicky.ClickyService',
    'analytical.services.crazyegg.CrazyEggService',
    'analytical.services.google_analytics.GoogleAnalyticsService',
    'analytical.services.kissinsights.KissInsightsService',
    'analytical.services.kissmetrics.KissMetricsService',
    'analytical.services.mixpanel.MixpanelService',
    'analytical.services.optimizely.OptimizelyService',
]


enabled_services = None
def get_enabled_services(reload=False):
    global enabled_services
    if enabled_services is None or reload:
        enabled_services = load_services()
    return enabled_services

def load_services():
    enabled_services = []
    try:
        service_paths = settings.ANALYTICAL_SERVICES
        autoload = False
    except AttributeError:
        service_paths = DEFAULT_SERVICES
        autoload = True
    for path in service_paths:
        try:
            module, attr = path.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured(
                        'error importing analytical service %s: "%s"'
                            % (module, e))
            try:
                service = getattr(mod, attr)()
            except AttributeError:
                raise ImproperlyConfigured(
                        'module "%s" does not define service "%s"'
                            % (module, attr))
            enabled_services.append(service)
        except ImproperlyConfigured, e:
            if autoload:
                _log.debug('not loading analytical service "%s": %s',
                        path, e)
            else:
                raise
    return enabled_services

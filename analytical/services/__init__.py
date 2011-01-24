"""
Analytics services.
"""

import logging

from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured


_log = logging.getLogger(__name__)

DEFAULT_SERVICES = [
    'analytical.services.chartbeat.ChartbeatService',
    'analytical.services.clicky.ClickyService',
    'analytical.services.crazy_egg.CrazyEggService',
    'analytical.services.google_analytics.GoogleAnalyticsService',
    'analytical.services.kiss_insights.KissInsightsService',
    'analytical.services.kiss_metrics.KissMetricsService',
    'analytical.services.mixpanel.MixpanelService',
    'analytical.services.optimizely.OptimizelyService',
]


enabled_services = None
def get_enabled_services():
    global enabled_services
    if enabled_services is None:
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
            service = _load_service(path)
            enabled_services.append(service)
        except ImproperlyConfigured, e:
            if autoload:
                _log.debug('not loading analytical service "%s": %s',
                        path, e)
            else:
                raise
    return enabled_services

def _load_service(path):
    module, attr = path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
                'error importing analytical service %s: "%s"' % (module, e))
    try:
        service = getattr(mod, attr)()
    except (AttributeError, TypeError):
        raise ImproperlyConfigured(
                'module "%s" does not define callable service "%s"'
                % (module, attr))
    return service

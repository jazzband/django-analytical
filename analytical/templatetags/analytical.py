"""
Analytical template tags.
"""

import logging

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import Node, TemplateSyntaxError
from django.utils.importlib import import_module


DEFAULT_SERVICES = [
    'analytical.chartbeat.chartbeat_service',
    'analytical.clicky.clicky_service',
    'analytical.crazy_egg.crazy_egg_service',
    'analytical.google_analytics.google_analytics_service',
    'analytical.hubspot.hubspot_service',
    'analytical.kiss_insights.kiss_insights_service',
    'analytical.kiss_metrics.kiss_metrics_service',
    'analytical.mixpanel.MixpanelService',
    'analytical.optimizely.OptimizelyService',
]
LOCATIONS = ['head_top', 'head_bottom', 'body_top', 'body_bottom']


_log = logging.getLogger(__name__)
register = template.Library()


def _location_tag(location):
    def tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
        return AnalyticalNode(location)
    return tag

for loc in LOCATIONS:
    register.tag('analytical_%s' % loc, _location_tag(loc))


class AnalyticalNode(Node):
    def __init__(self, location):
        self.nodes = template_nodes[location]

    def render(self, context):
        return "".join([node.render(context) for node in self.nodes])


def _load_template_nodes():
    location_nodes = dict((loc, []) for loc in LOCATIONS)
    try:
        service_paths = settings.ANALYTICAL_SERVICES
        autoload = False
    except AttributeError:
        service_paths = DEFAULT_SERVICES
        autoload = True
    for path in service_paths:
        try:
            service = _import_path(path)
            for location in LOCATIONS:
                node_path = service.get(location)
                if node_path is not None:
                    node_cls = _import_path(node_path)
                    node = node_cls()
                    location_nodes[location].append(node)
        except ImproperlyConfigured, e:
            if autoload:
                _log.debug("not loading analytical service '%s': %s",
                        path, e)
            else:
                raise
    return location_nodes

def _import_path(path):
    mod_name, attr_name = path.rsplit('.', 1)
    mod = import_module(mod_name)
    return getattr(mod, attr_name)

template_nodes = _load_template_nodes()

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
    'analytical.templatetags.chartbeat.service',
    'analytical.templatetags.clicky.service',
    'analytical.templatetags.crazy_egg.service',
    'analytical.templatetags.google_analytics.service',
    'analytical.templatetags.hubspot.service',
    'analytical.templatetags.kiss_insights.service',
    'analytical.templatetags.kiss_metrics.service',
    'analytical.templatetags.mixpanel.service',
    'analytical.templatetags.optimizely.service',
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
    try:
        service_paths = settings.ANALYTICAL_SERVICES
        autoload = False
    except AttributeError:
        service_paths = DEFAULT_SERVICES
        autoload = True
    services = _get_services(service_paths)
    location_nodes = dict((loc, []) for loc in LOCATIONS)
    for location in LOCATIONS:
        node_tuples = []
        for service in services:
            node_tuple = service.get(location)
            if node_tuple is not None:
                if not isinstance(node_tuple, tuple):
                    node_tuple = (node_tuple, None)
                node_tuples[location].append(node_tuple)
        location_nodes[location] = _get_nodes(node_tuples, autoload)
    return location_nodes

def _get_nodes(node_tuples, autoload):
    nodes = []
    node_sort_key = lambda n: {'first': -1, None: 0, 'last': 1}[n[1]]
    for node_tuple in sorted(node_tuples, key=node_sort_key):
        node_cls = node_tuple[0]
        try:
            nodes.append(node_cls())
        except ImproperlyConfigured, e:
            if autoload:
                _log.debug("not loading analytical service '%s': %s",
                        node_cls.__module__, e)
                continue
            else:
                raise
    return nodes

def _get_services(paths, autoload):
    services = []
    for path in paths:
        mod_name, attr_name = path.rsplit('.', 1)
        try:
            mod = import_module(mod_name)
        except ImportError, e:
            if autoload:
                _log.exception(e)
                continue
            else:
                raise
        try:
            service = getattr(mod, attr_name)
        except AttributeError, e:
            if autoload:
                _log.debug("not loading analytical service '%s': "
                        "module '%s' does not provide attribute '%s'",
                        path, mod_name, attr_name)
                continue
            else:
                raise
        services.append(service)
    return services

template_nodes = _load_template_nodes()

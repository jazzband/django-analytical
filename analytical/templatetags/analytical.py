"""
Analytical template tags and filters.
"""

from __future__ import absolute_import

import logging

from django import template
from django.template import Node, TemplateSyntaxError
from django.utils.importlib import import_module
from analytical.utils import AnalyticalException


TAG_LOCATIONS = ['head_top', 'head_bottom', 'body_top', 'body_bottom']
TAG_POSITIONS = ['first', None, 'last']
TAG_MODULES = [
    'analytical.chartbeat',
    'analytical.clicky',
    'analytical.crazy_egg',
    'analytical.google_analytics',
    'analytical.gosquared',
    'analytical.hubspot',
    'analytical.kiss_insights',
    'analytical.kiss_metrics',
    'analytical.mixpanel',
    'analytical.olark',
    'analytical.optimizely',
    'analytical.performable',
    'analytical.reinvigorate',
    'analytical.snapengage',
    'analytical.spring_metrics',
    'analytical.woopra',
]


logger = logging.getLogger(__name__)
register = template.Library()


def _location_tag(location):
    def analytical_tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
        return AnalyticalNode(location)
    return analytical_tag

for loc in TAG_LOCATIONS:
    register.tag('analytical_%s' % loc, _location_tag(loc))


class AnalyticalNode(Node):
    def __init__(self, location):
        self.nodes = [node_cls() for node_cls in template_nodes[location]]

    def render(self, context):
        return "".join([node.render(context) for node in self.nodes])


def _load_template_nodes():
    template_nodes = dict((l, dict((p, []) for p in TAG_POSITIONS))
            for l in TAG_LOCATIONS)
    def add_node_cls(location, node, position=None):
        template_nodes[location][position].append(node)
    for path in TAG_MODULES:
        module = _import_tag_module(path)
        try:
            module.contribute_to_analytical(add_node_cls)
        except AnalyticalException, e:
            logger.debug("not loading tags from '%s': %s", path, e)
    for location in TAG_LOCATIONS:
        template_nodes[location] = sum((template_nodes[location][p]
                for p in TAG_POSITIONS), [])
    return template_nodes

def _import_tag_module(path):
    app_name, lib_name = path.rsplit('.', 1)
    return import_module("%s.templatetags.%s" % (app_name, lib_name))

template_nodes = _load_template_nodes()

"""
Analytical template tags and filters.
"""

import logging
from importlib import import_module

from django import template
from django.template import Node, TemplateSyntaxError

from analytical.utils import AnalyticalException

TAG_LOCATIONS = ['head_top', 'head_bottom', 'body_top', 'body_bottom']
TAG_POSITIONS = ['first', None, 'last']
TAG_MODULES = [
    'analytical.chartbeat',
    'analytical.clickmap',
    'analytical.clicky',
    'analytical.crazy_egg',
    'analytical.facebook_pixel',
    'analytical.gauges',
    'analytical.google_analytics',
    'analytical.google_analytics_js',
    'analytical.google_analytics_gtag',
    'analytical.gosquared',
    'analytical.heap',
    'analytical.hotjar',
    'analytical.hubspot',
    'analytical.intercom',
    'analytical.kiss_insights',
    'analytical.kiss_metrics',
    'analytical.luckyorange',
    'analytical.matomo',
    'analytical.mixpanel',
    'analytical.olark',
    'analytical.optimizely',
    'analytical.performable',
    'analytical.piwik',
    'analytical.rating_mailru',
    'analytical.snapengage',
    'analytical.spring_metrics',
    'analytical.uservoice',
    'analytical.woopra',
    'analytical.yandex_metrica',
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
    template_nodes = {loc: {pos: [] for pos in TAG_POSITIONS} for loc in TAG_LOCATIONS}

    def add_node_cls(location, node, position=None):
        template_nodes[location][position].append(node)

    for path in TAG_MODULES:
        module = _import_tag_module(path)
        try:
            module.contribute_to_analytical(add_node_cls)
        except AnalyticalException as e:
            logger.debug("not loading tags from '%s': %s", path, e)
    for location in TAG_LOCATIONS:
        template_nodes[location] = sum((template_nodes[location][p]
                                        for p in TAG_POSITIONS), [])
    return template_nodes


def _import_tag_module(path):
    app_name, lib_name = path.rsplit('.', 1)
    return import_module("%s.templatetags.%s" % (app_name, lib_name))


template_nodes = _load_template_nodes()

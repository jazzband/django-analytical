"""
Analytical template tags and filters.
"""

import logging

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import Node, TemplateSyntaxError
from django.utils.importlib import import_module

from analytical.templatetags import chartbeat, clicky, crazy_egg, \
        google_analytics, hubspot, kiss_insights, kiss_metrics, mixpanel, \
        optimizely


TAG_NODES = {
    'head_top': [
        chartbeat.ChartbeatTopNode,  # Chartbeat should come first
        kiss_metrics.KissMetricsNode,
        optimizely.OptimizelyNode,
    ],
    'head_bottom': [
        google_analytics.GoogleAnalyticsNode,
        mixpanel.MixpanelNode,
    ],
    'body_top': [
        kiss_insights.KissInsightsNode,
    ],
    'body_bottom': [
        clicky.ClickyNode,
        crazy_egg.CrazyEggNode,
        hubspot.HubSpotNode,
        chartbeat.ChartbeatBottomNode, # Chartbeat should come last
    ],
}


logger = logging.getLogger(__name__)
register = template.Library()


def _location_tag(location):
    def analytical_tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
        return AnalyticalNode(location)
    return analytical_tag

for loc in TAG_NODES.keys():
    register.tag('analytical_%s' % loc, _location_tag(loc))


class AnalyticalNode(Node):
    def __init__(self, location):
        self.nodes = template_nodes[location]

    def render(self, context):
        return "".join([node.render(context) for node in self.nodes])


def _load_template_nodes():
    location_nodes = {}
    for location, node_classes in TAG_NODES.items():
        location_nodes[location] = []
        for node_class in node_classes:
            try:
                node = node_class()
            except ImproperlyConfigured, e:
                logger.debug("not loading analytical service '%s': %s",
                        node_class.name, e)
            location_nodes.append(node)
    return location_nodes

template_nodes = _load_template_nodes()

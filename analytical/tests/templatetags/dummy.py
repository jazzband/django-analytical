"""
Dummy testing template tags and filters.
"""

from __future__ import absolute_import

from django.template import Library, Node, TemplateSyntaxError

from analytical.templatetags.analytical import TAG_LOCATIONS


register = Library()


def _location_node(location):
    class DummyNode(Node):
        def render(self, context):
            return "<!-- dummy_%s -->" % location
    return DummyNode

_location_nodes = dict((l, _location_node(l)) for l in TAG_LOCATIONS)


def _location_tag(location):
    def dummy_tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
        return _location_nodes[location]
    return dummy_tag

for loc in TAG_LOCATIONS:
    register.tag('dummy_%s' % loc, _location_tag(loc))


def contribute_to_analytical(add_node_cls):
    for location in TAG_LOCATIONS:
        add_node_cls(location, _location_nodes[location])

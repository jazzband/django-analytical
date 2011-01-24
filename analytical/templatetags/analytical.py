"""
Analytical template tags.
"""
from __future__ import absolute_import

from django import template
from django.conf import settings
from django.template import Node, TemplateSyntaxError, Variable

from analytical.services import get_enabled_services


HTML_COMMENT_CODE = "<!-- Analytical disabled on internal IP address\n%s\n-->"
JS_COMMENT_CODE = "/* %s */"
SCRIPT_CODE = """<script type="text/javascript">%s</script>"""


register = template.Library()


def _location_tag(location):
    def tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
        return AnalyticalNode(location)
    return tag

for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
    register.tag('analytical_setup_%s' % l, _location_tag(l))


class AnalyticalNode(Node):
    def __init__(self, location):
        self.location = location
        self.render_func_name = "render_%s" % self.location
        self.internal_ips = getattr(settings, 'ANALYTICAL_INTERNAL_IPS',
                getattr(settings, 'INTERNAL_IPS', ()))

    def render(self, context):
        result = "".join([self._render_service(service, context)
                for service in get_enabled_services()])
        if not result:
            return ""
        if self._is_internal_ip(context):
            return HTML_COMMENT_CODE % result
        return result

    def _render_service(self, service, context):
        func = getattr(service, self.render_func_name)
        return func(context)

    def _is_internal_ip(self, context):
        try:
            request = context['request']
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR',
                    request.META.get('REMOTE_ADDR', ''))
            return remote_ip in self.internal_ips
        except KeyError, AttributeError:
            return False


def event(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' tag takes at least one argument"
                % bits[0])
    properties = _parse_properties(bits[0], bits[2:])
    return EventNode(bits[1], properties)

register.tag('event', event)


class EventNode(Node):
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties

    def render(self, context):
        props = dict((var, Variable(val).resolve(context))
                for var, val in self.properties)
        result = "".join([service.render_js_event(props)
                for service in get_enabled_services()])
        if not result:
            return ""
        if self._is_internal_ip(context):
            return JS_COMMENT_CODE % result
        return result


def _parse_properties(tag_name, bits):
    properties = []
    for bit in bits:
        try:
            properties.append(bit.split('=', 1))
        except IndexError:
            raise TemplateSyntaxError("'%s' tag argument must be of the form "
                    " property=value: '%s'" % (tag_name, bit))
    return properties

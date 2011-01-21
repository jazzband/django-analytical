"""
Analytical template tags.
"""
from __future__ import absolute_import

from django import template
from django.conf import settings
from django.template import Node, TemplateSyntaxError

from analytical.services import get_enabled_services


DISABLE_CODE = "<!-- Analytical disabled on internal IP address\n%s\n-->"


register = template.Library()


def _location_tag(location):
    def tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            raise TemplateSyntaxError("'%s' tag takes no arguments" % bits[0])
        return AnalyticalNode(location)
    return tag

for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
    register.tag('analytical_%s' % l, _location_tag(l))


class AnalyticalNode(Node):
    def __init__(self, location):
        self.location = location
        self.render_func_name = "render_%s" % self.location
        self.internal_ips = getattr(settings, 'ANALYTICAL_INTERNAL_IPS',
                getattr(settings, 'INTERNAL_IPS', ()))

    def render(self, context):
        html = "".join([self._render_service(service, context)
                for service in get_enabled_services()])
        if not html:
            return ""
#        if self._is_internal_ip(context):
#            return DISABLE_CODE % html
        return html

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

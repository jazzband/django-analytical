"""
Spring Metrics template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_identity, is_internal_ip, disable_html, \
        get_required_setting


TRACKING_ID_RE = re.compile(r'^[0-9a-f]+$')
TRACKING_CODE = """
    <script type='text/javascript'>
     var _springMetq = _springMetq || [];
     _springMetq.push(['id', '%(tracking_id)s']);
     %(custom_commands)s
     (
      function(){
       var s = document.createElement('script');
       s.type = 'text/javascript';
       s.async = true;
       s.src = ('https:' == document.location.protocol ? 'https://d3rmnwi2tssrfx.cloudfront.net/a.js' : 'http://static.springmetrics.com/a.js');
       var x = document.getElementsByTagName('script')[0];
       x.parentNode.insertBefore(s, x);
      }
     )();
    </script>
"""


register = Library()


@register.tag
def spring_metrics(parser, token):
    """
    Spring Metrics tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Spring Metrics Tracking ID in the
    ``SPRING_METRICS_TRACKING_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return SpringMetricsNode()

class SpringMetricsNode(Node):
    def __init__(self):
        self.tracking_id = get_required_setting('SPRING_METRICS_TRACKING_ID',
            TRACKING_ID_RE, "must be a hexadecimal string")

    def render(self, context):
        custom = {}
        for dict_ in context:
            for var, val in dict_.items():
                if var.startswith('spring_metrics_'):
                    custom[var[15:]] = val
        if 'email' not in custom:
            identity = get_identity(context, 'spring_metrics',
                    lambda u: u.email)
            if identity is not None:
                custom['email'] = identity

        html = TRACKING_CODE % {'tracking_id': self.tracking_id,
                'custom_commands': self._generate_custom_javascript(custom)}
        if is_internal_ip(context, 'SPRING_METRICS'):
            html = disable_html(html, 'Spring Metrics')
        return html

    def _generate_custom_javascript(self, vars):
        commands = ("_springMetq.push(['%s', '%s']);" % (var, val)
                for var, val in vars.items())
        return " ".join(commands)


def contribute_to_analytical(add_node):
    SpringMetricsNode()  # ensure properly configured
    add_node('head_bottom', SpringMetricsNode)

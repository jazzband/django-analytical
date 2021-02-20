"""
Spring Metrics template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    is_internal_ip,
)

TRACKING_ID_RE = re.compile(r'^[0-9a-f]+$')
TRACKING_CODE = """
    <script type='text/javascript'>
     var _springMetq = _springMetq || [];
     _springMetq.push(['id', '%(tracking_id)s']);
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
     %(custom_commands)s
    </script>
"""  # noqa

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
        self.tracking_id = get_required_setting(
                'SPRING_METRICS_TRACKING_ID',
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

        html = TRACKING_CODE % {
            'tracking_id': self.tracking_id,
            'custom_commands': self._generate_custom_javascript(custom),
        }
        if is_internal_ip(context, 'SPRING_METRICS'):
            html = disable_html(html, 'Spring Metrics')
        return html

    def _generate_custom_javascript(self, params):
        commands = []
        convert = params.pop('convert', None)
        if convert is not None:
            commands.append("_springMetq.push(['convert', '%s'])" % convert)
        commands.extend("_springMetq.push(['setdata', {'%s': '%s'}]);"
                        % (var, val) for var, val in params.items())
        return " ".join(commands)


def contribute_to_analytical(add_node):
    SpringMetricsNode()  # ensure properly configured
    add_node('head_bottom', SpringMetricsNode)

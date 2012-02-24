"""
Gaug.es template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import is_internal_ip, disable_html, get_required_setting

SITE_ID_RE = re.compile(r'[\da-f]+$')
TRACKING_CODE = """
    <script type="text/javascript">
      var _gauges = _gauges || [];
      (function() {
        var t   = document.createElement('script');
        t.type  = 'text/javascript';
        t.async = true;
        t.id    = 'gauges-tracker';
        t.setAttribute('data-site-id', '%(site_id)s');
        t.src = '//secure.gaug.es/track.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(t, s);
      })();
    </script>
"""

register = Library()


@register.tag
def gauges(parser, token):
    """
    Gaug.es template tag.

    Renders Javascript code to gaug.es testing.  You must supply
    your Site ID account number in the ``GAUGES_SITE_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return GaugesNode()


class GaugesNode(Node):
    def __init__(self):
        self.site_id = get_required_setting(
                'GAUGES_SITE_ID', SITE_ID_RE,
                "must be a string looking like 'XXXXXXX'")

    def render(self, context):
        html = TRACKING_CODE % {'site_id': self.site_id}
        if is_internal_ip(context, 'GAUGES'):
            html = disable_html(html, 'Gauges')
        return html


def contribute_to_analytical(add_node):
    GaugesNode()
    add_node('head_bottom', GaugesNode)

"""
Google Analytics template tags and filters, using the new analytics.js library.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_required_setting,
    is_internal_ip,
)

PROPERTY_ID_RE = re.compile(r'^UA-\d+-\d+$')
SETUP_CODE = """
<script async src="https://www.googletagmanager.com/gtag/js?id={property_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{property_id}');
</script>
"""

register = Library()


@register.tag
def google_analytics_gtag(parser, token):
    """
    Google Analytics tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your website property ID (as a string) in the
    ``GOOGLE_ANALYTICS_GTAG_PROPERTY_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return GoogleAnalyticsGTagNode()


class GoogleAnalyticsGTagNode(Node):
    def __init__(self):
        self.property_id = get_required_setting(
            'GOOGLE_ANALYTICS_GTAG_PROPERTY_ID', PROPERTY_ID_RE,
            "must be a string looking like 'UA-XXXXXX-Y'")

    def render(self, context):
        html = SETUP_CODE.format(
            property_id=self.property_id,
        )
        if is_internal_ip(context, 'GOOGLE_ANALYTICS'):
            html = disable_html(html, 'Google Analytics')
        return html


def contribute_to_analytical(add_node):
    GoogleAnalyticsGTagNode()  # ensure properly configured
    add_node('head_top', GoogleAnalyticsGTagNode)

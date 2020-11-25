"""
Google Analytics template tags and filters, using the new analytics.js library.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    is_internal_ip,
)

PROPERTY_ID_RE = re.compile(r'^UA-\d+-\d+$|^G-[a-zA-Z0-9]+$|^AW-[a-zA-Z0-9]+$|^DC-[a-zA-Z0-9]+$')
SETUP_CODE = """
<script async src="https://www.googletagmanager.com/gtag/js?id={property_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  {extra}
  gtag('config', '{property_id}');
</script>
"""

GTAG_SET_CODE = """gtag('set', {{'{key}': '{value}'}});"""

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
            '''must be a string looking like one of these patterns
            ('UA-XXXXXX-Y' , 'AW-XXXXXXXXXX',
            'G-XXXXXXXX', 'DC-XXXXXXXX')''')

    def render(self, context):
        other_fields = {}

        identity = get_identity(context)
        if identity is not None:
            other_fields['user_id'] = identity

        extra = '\n'.join([
            GTAG_SET_CODE.format(key=key, value=value) for key, value in other_fields.items()
        ])
        html = SETUP_CODE.format(
            property_id=self.property_id,
            extra=extra,
        )
        if is_internal_ip(context, 'GOOGLE_ANALYTICS'):
            html = disable_html(html, 'Google Analytics')
        return html


def contribute_to_analytical(add_node):
    GoogleAnalyticsGTagNode()  # ensure properly configured
    add_node('head_top', GoogleAnalyticsGTagNode)

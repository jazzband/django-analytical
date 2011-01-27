"""
HubSpot template tags.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import get_required_setting, is_internal_ip, disable_html


PORTAL_ID_RE = re.compile(r'^\d+$')
DOMAIN_RE = re.compile(r'^[\w.-]+$')
TRACKING_CODE = """
    <script type="text/javascript" language="javascript">
    var hs_portalid = %(portal_id)s;
    var hs_salog_version = "2.00";
    var hs_ppa = "%(domain)s";
    document.write(unescape("%3Cscript src='" + document.location.protocol + "//" + hs_ppa + "/salog.js.aspx' type='text/javascript'%3E%3C/script%3E"));
    </script>
"""


register = Library()


@register.tag
def hubspot(parser, token):
    """
    HubSpot tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your portal ID (as a string) in the ``HUBSPOT_PORTAL_ID`` setting,
    and the website domain in ``HUBSPOT_DOMAIN``.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return HubSpotNode()

class HubSpotNode(Node):
    def __init__(self):
        self.site_id = get_required_setting('HUPSPOT_PORTAL_ID',
                PORTAL_ID_RE, "must be a (string containing a) number")
        self.domain = get_required_setting('HUPSPOT_DOMAIN',
                DOMAIN_RE, "must be an internet domain name")

    def render(self, context):
        html = TRACKING_CODE % {'portal_id': self.portal_id,
                'domain': self.domain}
        if is_internal_ip(context):
            html = disable_html(html, 'HubSpot')
        return html

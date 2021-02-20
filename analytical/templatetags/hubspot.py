"""
HubSpot template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

PORTAL_ID_RE = re.compile(r'^\d+$')
TRACKING_CODE = """
    <!-- Start of Async HubSpot Analytics Code -->
      <script type="text/javascript">
        (function(d,s,i,r) {
          if (d.getElementById(i)){return;}
          var n=d.createElement(s),e=d.getElementsByTagName(s)[0];
          n.id=i;n.src='//js.hs-analytics.net/analytics/'+(Math.ceil(new Date()/r)*r)+'/%(portal_id)s.js';
          e.parentNode.insertBefore(n, e);
        })(document,"script","hs-analytics",300000);
      </script>
    <!-- End of Async HubSpot Analytics Code -->
"""  # noqa

register = Library()


@register.tag
def hubspot(parser, token):
    """
    HubSpot tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your portal ID (as a string) in the ``HUBSPOT_PORTAL_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return HubSpotNode()


class HubSpotNode(Node):
    def __init__(self):
        self.portal_id = get_required_setting('HUBSPOT_PORTAL_ID', PORTAL_ID_RE,
                                              "must be a (string containing a) number")

    def render(self, context):
        html = TRACKING_CODE % {'portal_id': self.portal_id}
        if is_internal_ip(context, 'HUBSPOT'):
            html = disable_html(html, 'HubSpot')
        return html


def contribute_to_analytical(add_node):
    HubSpotNode()  # ensure properly configured
    add_node('body_bottom', HubSpotNode)

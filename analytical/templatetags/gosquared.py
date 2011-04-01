"""
GoSquared template tags and filters.
"""

from __future__ import absolute_import

import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_identity, get_user_from_context, \
        is_internal_ip, disable_html, get_required_setting


TOKEN_RE = re.compile(r'^\S+-\S+-\S+$')
TRACKING_CODE = """
    <script type="text/javascript">
      var GoSquared={};
      %(config)s
      (function(w){
        function gs(){
          w._gstc_lt=+(new Date); var d=document;
          var g = d.createElement("script"); g.type = "text/javascript"; g.async = true; g.src = "//d1l6p2sc9645hc.cloudfront.net/tracker.js";
          var s = d.getElementsByTagName("script")[0]; s.parentNode.insertBefore(g, s);
        }
        w.addEventListener?w.addEventListener("load",gs,false):w.attachEvent("onload",gs);
      })(window);
    </script>
"""
TOKEN_CODE = 'GoSquared.acct = "%s";'
IDENTIFY_CODE = 'GoSquared.UserName = "%s";'


register = Library()


@register.tag
def gosquared(parser, token):
    """
    GoSquared tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your GoSquared site token in the ``GOSQUARED_SITE_TOKEN`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return GoSquaredNode()

class GoSquaredNode(Node):
    def __init__(self):
        self.site_token = get_required_setting('GOSQUARED_SITE_TOKEN', TOKEN_RE,
                "must be a string looking like XXX-XXXXXX-X")

    def render(self, context):
        configs = [TOKEN_CODE % self.site_token]
        identity = get_identity(context, 'gosquared', self._identify)
        if identity:
            configs.append(IDENTIFY_CODE % identity)
        html = TRACKING_CODE % {
            'token': self.site_token,
            'config': ' '.join(configs),
        }
        if is_internal_ip(context, 'GOSQUARED'):
            html = disable_html(html, 'GoSquared')
        return html

    def _identify(self, user):
        name = user.get_full_name()
        if not name:
            name = user.username
        return name


def contribute_to_analytical(add_node):
    GoSquaredNode()  # ensure properly configured
    add_node('body_bottom', GoSquaredNode)

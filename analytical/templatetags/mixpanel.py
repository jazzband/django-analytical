"""
Mixpanel template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import is_internal_ip, disable_html, get_identity, \
        get_required_setting


MIXPANEL_API_TOKEN_RE = re.compile(r'^[0-9a-f]{32}$')
TRACKING_CODE = """
    <script type="text/javascript">
      var mpq = [];
      mpq.push(['init', '%(token)s']);
      %(commands)s
      (function(){var b,a,e,d,c;b=document.createElement("script");b.type="text/javascript";b.async=true;b.src=(document.location.protocol==="https:"?"https:":"http:")+"//api.mixpanel.com/site_media/js/api/mixpanel.js";a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(b,a);e=function(f){return function(){mpq.push([f].concat(Array.prototype.slice.call(arguments,0)))}};d=["init","track","track_links","track_forms","register","register_once","identify","name_tag","set_config"];for(c=0;c<d.length;c++){mpq[d[c]]=e(d[c])}})();
    </script>
"""
IDENTIFY_CODE = "mpq.push(['identify', '%s']);"
EVENT_CODE = "mpq.push(['track', '%(name)s', %(properties)s]);"
EVENT_CONTEXT_KEY = 'mixpanel_event'

register = Library()


@register.tag
def mixpanel(parser, token):
    """
    Mixpanel tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Mixpanel token in the ``MIXPANEL_API_TOKEN`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return MixpanelNode()

class MixpanelNode(Node):
    def __init__(self):
        self.token = get_required_setting(
                'MIXPANEL_API_TOKEN', MIXPANEL_API_TOKEN_RE,
                "must be a string containing a 32-digit hexadecimal number")

    def render(self, context):
        commands = []
        identity = get_identity(context, 'mixpanel')
        if identity is not None:
            commands.append(IDENTIFY_CODE % identity)
        try:
            name, properties = context[EVENT_CONTEXT_KEY]
            commands.append(EVENT_CODE % {'name': name,
                    'properties': simplejson.dumps(properties)})
        except KeyError:
            pass
        html = TRACKING_CODE % {'token': self.token,
                'commands': " ".join(commands)}
        if is_internal_ip(context, 'MIXPANEL'):
            html = disable_html(html, 'Mixpanel')
        return html


def contribute_to_analytical(add_node):
    MixpanelNode()  # ensure properly configured
    add_node('head_bottom', MixpanelNode)

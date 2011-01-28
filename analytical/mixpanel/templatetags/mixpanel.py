"""
Mixpanel template tags.
"""

import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import is_internal_ip, disable_html


MIXPANEL_TOKEN_RE = re.compile(r'^[0-9a-f]{32}$')
TRACKING_CODE = """
    <script type="text/javascript">
      var mpq = [];
      mpq.push(['init', '%(token)s']);
      %(commands)s
      (function() {
        var mp = document.createElement("script"); mp.type = "text/javascript"; mp.async = true;
        mp.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + "//api.mixpanel.com/site_media/js/api/mixpanel.js";
        var s = document.getElementsByTagName("script")[0]; s.parentNode.insertBefore(mp, s);
      })();
    </script>
"""
IDENTIFY_CODE = "mpq.push(['identify', '%s']);"
EVENT_CODE = "mpq.push(['track', '%(name)s', %(properties)s]);"
EVENT_CONTEXT_KEY = 'mixpanel_metrics_event'

register = Library()


@register.tag
def mixpanel(parser, token):
    """
    Mixpanel tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Mixpanel token in the ``MIXPANEL_TOKEN`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return MixpanelNode()

class MixpanelNode(Node):
    def __init__(self):
        self.token = self.get_required_setting('MIXPANEL_TOKEN',
                MIXPANEL_TOKEN_RE,
                "must be a string containing a 32-digit hexadecimal number")

    def render(self, context):
        commands = []
        identity = self.get_identity(context)
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
        if is_internal_ip(context):
            html = disable_html(html, 'Mixpanel')
        return html

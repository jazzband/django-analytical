"""
Mixpanel service.
"""

import re

from django.utils import simplejson

from analytical.services.base import AnalyticalService


MIXPANEL_TOKEN_RE = re.compile(r'^[0-9a-f]{32}$')
SETUP_CODE = """
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


class MixpanelService(AnalyticalService):
    def __init__(self):
        self.token = self.get_required_setting('MIXPANEL_TOKEN',
                MIXPANEL_TOKEN_RE,
                "must be a string containing a 32-digit hexadecimal number")

    def render_head_bottom(self, context):
        commands = []
        identity = self.get_identity(context)
        if identity is not None:
            commands.append(IDENTIFY_CODE % identity)
        return SETUP_CODE % {'token': self.token,
                'commands': " ".join(commands)}

    def render_event(self, name, properties):
        return EVENT_CODE % {'name': name,
                'properties': simplejson.dumps(properties)}

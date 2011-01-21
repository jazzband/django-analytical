"""
Mixpanel service.
"""

import re

from analytical.services.base import AnalyticalService


MIXPANEL_TOKEN_RE = re.compile(r'^[0-9a-f]{32}$')
TRACKING_CODE = """
    <script type='text/javascript'>
        var mp_protocol = (('https:' == document.location.protocol) ? 'https://' : 'http://');
        document.write(unescape('%%3Cscript src="' + mp_protocol + 'api.mixpanel.com/site_media/js/api/mixpanel.js" type="text/javascript"%%3E%%3C/script%%3E'));
    </script>
    <script type='text/javascript'>
        try {
            var mpmetrics = new MixpanelLib('%(token)s');
        } catch(err) {
            null_fn = function () {};
            var mpmetrics = {track: null_fn, track_funnel: null_fn,
                    register: null_fn, register_once: null_fn,
                    register_funnel: null_fn};
        }
    </script>
"""


class MixpanelService(AnalyticalService):
    KEY = 'mixpanel'

    def __init__(self):
        self.token = self.get_required_setting('MIXPANEL_TOKEN',
                MIXPANEL_TOKEN_RE,
                "must be a string containing a 32-digit hexadecimal number")

    def render_body_bottom(self, context):
        return TRACKING_CODE % {'token': self.token}

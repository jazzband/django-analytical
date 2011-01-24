"""
Clicky service.
"""

import re

from django.utils import simplejson

from analytical.services.base import AnalyticalService


SITE_ID_RE = re.compile(r'^\d{8}$')
SETUP_CODE = """
    <script type="text/javascript">
    var clicky = { log: function(){ return; }, goal: function(){ return; }};
    var clicky_site_id = %(site_id)s;
    var clicky_custom = %(custom)s;
    (function() {
      var s = document.createElement('script');
      s.type = 'text/javascript';
      s.async = true;
      s.src = ( document.location.protocol == 'https:' ? 'https://static.getclicky.com/js' : 'http://static.getclicky.com/js' );
      ( document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0] ).appendChild( s );
    })();
    </script>
    <noscript><p><img alt="Clicky" width="1" height="1" src="http://in.getclicky.com/%(site_id)sns.gif" /></p></noscript>
"""
CUSTOM_CONTEXT_KEY = 'clicky_custom'


class ClickyService(AnalyticalService):
    def __init__(self):
        self.site_id = self.get_required_setting('CLICKY_SITE_ID', SITE_ID_RE,
                "must be a string containing an eight-digit number")

    def render_body_bottom(self, context):
        custom = {
            'session': {
                'username': self.get_identity(context),
            }
        }
        custom.update(context.get(CUSTOM_CONTEXT_KEY, {}))
        return SETUP_CODE % {'site_id': self.site_id,
                'custom': simplejson.dumps(custom)}

    def _convert_properties(self):
        pass

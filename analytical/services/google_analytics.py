"""
Google Analytics service.
"""

import re

from analytical.services.base import AnalyticalService


PROPERTY_ID_RE = re.compile(r'^UA-\d+-\d+$')
TRACKING_CODE = """
    <script type="text/javascript">

      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '%(property_id)s']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script>
"""


class GoogleAnalyticsService(AnalyticalService):
    KEY = 'google_analytics'

    def __init__(self):
        self.property_id = self.get_required_setting(
                'GOOGLE_ANALYTICS_PROPERTY_ID', PROPERTY_ID_RE,
                "must be a string looking like 'UA-XXXXXX-Y'")

    def render_head_bottom(self, context):
        return TRACKING_CODE % {'property_id': self.property_id}

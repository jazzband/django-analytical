"""
KISSmetrics service.
"""

import re

from analytical.services.base import AnalyticalService


API_KEY_RE = re.compile(r'^[0-9a-f]{40}$')
TRACKING_CODE = """
    <script type="text/javascript">
      var _kmq = _kmq || [];
      function _kms(u){
        setTimeout(function(){
          var s = document.createElement('script');
          s.type = 'text/javascript';
          s.async = true;
          s.src = u;
          var f = document.getElementsByTagName('script')[0];
          f.parentNode.insertBefore(s, f);
        }, 1);
      }
      _kms('//i.kissmetrics.com/i.js');
      _kms('//doug1izaerwt3.cloudfront.net/%(api_key)s.1.js');
    </script>
"""


class KissMetricsService(AnalyticalService):
    KEY = 'kissmetrics'

    def __init__(self):
        self.api_key = self.get_required_setting('KISSMETRICS_API_KEY',
                API_KEY_RE,
                "must be a string containing a 40-digit hexadecimal number")

    def render_head_top(self, context):
        return TRACKING_CODE % {'api_key': self.api_key}

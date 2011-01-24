"""
KISSmetrics service.
"""

import re

from django.utils import simplejson

from analytical.services.base import AnalyticalService


API_KEY_RE = re.compile(r'^[0-9a-f]{40}$')
SETUP_CODE = """
    <script type="text/javascript">
      var _kmq = _kmq || [];
      %(commands)s
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
IDENTIFY_CODE = "_kmq.push(['identify', '%s']);"
JS_EVENT_CODE = "_kmq.push(['record', '%(name)s', %(properties)s]);"


class KissMetricsService(AnalyticalService):
    def __init__(self):
        self.api_key = self.get_required_setting('KISS_METRICS_API_KEY',
                API_KEY_RE,
                "must be a string containing a 40-digit hexadecimal number")

    def render_head_top(self, context):
        commands = []
        identity = self.get_identity(context)
        if identity is not None:
            commands.append(IDENTIFY_CODE % identity)
        return SETUP_CODE % {'api_key': self.api_key,
                'commands': commands}

    def render_event(self, name, properties):
        return JS_EVENT_CODE % {'name': name,
                'properties': simplejson.dumps(properties)}

"""
Chartbeat service.
"""

import re

from django.contrib.sites.models import Site, RequestSite
from django.core.exceptions import ImproperlyConfigured
from django.utils import simplejson

from analytical.services.base import AnalyticalService


USER_ID_RE = re.compile(r'^\d{5}$')
INIT_CODE = """<script type="text/javascript">var _sf_startpt=(new Date()).getTime()</script>"""
SETUP_CODE = """
<script type="text/javascript">
    var _sf_async_config=%(config)s;
    (function(){
      function loadChartbeat() {
        window._sf_endpt=(new Date()).getTime();
        var e = document.createElement('script');
        e.setAttribute('language', 'javascript');
        e.setAttribute('type', 'text/javascript');
        e.setAttribute('src',
           (("https:" == document.location.protocol) ? "https://a248.e.akamai.net/chartbeat.download.akamai.com/102508/" : "http://static.chartbeat.com/") +
           "js/chartbeat.js");
        document.body.appendChild(e);
      }
      var oldonload = window.onload;
      window.onload = (typeof window.onload != 'function') ?
         loadChartbeat : function() { oldonload(); loadChartbeat(); };
    })();
</script>
"""
DOMAIN_CONTEXT_KEY = 'chartbeat_domain'


class ChartbeatService(AnalyticalService):
    def __init__(self):
        self.user_id = self.get_required_setting(
                'CHARTBEAT_USER_ID', USER_ID_RE,
                "must be a string containing an five-digit number")

    def render_head_top(self, context):
        return INIT_CODE

    def render_body_bottom(self, context):
        config = {'uid': self.user_id}
        try:
            config['domain'] = context[DOMAIN_CONTEXT_KEY]
        except KeyError:
            try:
                config['domain'] = Site.objects.get_current().domain
            except (ImproperlyConfigured, Site.DoesNotExist, AttributeError):
                pass
        return SETUP_CODE % {'config': simplejson.dumps(config)}

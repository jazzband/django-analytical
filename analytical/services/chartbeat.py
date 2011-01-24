"""
Chartbeat service.
"""

import re

from django.contrib.sites.models import Site, RequestSite
from django.core.exceptions import ImproperlyConfigured

from analytical.services.base import AnalyticalService


USER_ID_RE = re.compile(r'^\d{5}$')
INIT_CODE = """<script type="text/javascript">var _sf_startpt=(new Date()).getTime()</script>"""
SETUP_CODE = """
<script type="text/javascript">
    var _sf_async_config={uid:%(user_id)s,domain:"%(domain)s"};
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
        return SETUP_CODE % {'user_id': self.user_id,
                'domain': self._get_domain(context)}

    def _get_domain(self, context):
        try:
            return context[DOMAIN_CONTEXT_KEY]
        except KeyError:
            pass
        try:
            return Site.objects.get_current().domain
        except ImproperlyConfigured:
            pass
        try:
            request = context['request']
            return RequestSite(request).domain
        except (KeyError, AttributeError):
            raise KeyError("could not find access either '%s' or 'request' "
                    "in the template context and 'django.contrib.sites' is "
                    "not in INSTALLED_APPS" % DOMAIN_CONTEXT_KEY)

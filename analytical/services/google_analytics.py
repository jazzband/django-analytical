"""
Google Analytics service.
"""

import re

from analytical.services.base import AnalyticalService


PROPERTY_ID_RE = re.compile(r'^UA-\d+-\d+$')
SETUP_CODE = """
    <script type="text/javascript">

      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '%(property_id)s']);
      %(commands)s

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script>
"""
TRACK_CODE = "_gaq.push(['_trackPageview']);"
CUSTOM_VARS_CONTEXT_KEY = "google_analytics_custom_vars"
CUSTOM_VAR_CODE = "_gaq.push(['_setCustomVar', %(index)d, '%(name)s', " \
        "'%(value)s', %(scope)d]);"

class GoogleAnalyticsService(AnalyticalService):
    def __init__(self):
        self.property_id = self.get_required_setting(
                'GOOGLE_ANALYTICS_PROPERTY_ID', PROPERTY_ID_RE,
                "must be a string looking like 'UA-XXXXXX-Y'")

    def render_head_bottom(self, context):
        commands = self._get_custom_var_commands(context)
        commands.append(TRACK_CODE)
        return SETUP_CODE % {'property_id': self.property_id,
                'commands': " ".join(commands)}

    def _get_custom_var_commands(self, context):
        commands = []
        vardefs = context.get(CUSTOM_VARS_CONTEXT_KEY, [])
        for vardef in vardefs:
            index = vardef[0]
            if not 1 <= index <= 5:
                raise ValueError("Google Analytics custom variable index must "
                        "be between 1 and 5: %s" % index)
            name = vardef[1]
            value = vardef[2]
            if len(vardef) >= 4:
                scope = vardef[3]
            else:
                scope = 2
            commands.append(CUSTOM_VAR_CODE % locals())
        return commands

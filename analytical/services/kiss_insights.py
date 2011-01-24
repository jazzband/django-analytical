"""
KISSinsights service.
"""

import re

from analytical.services.base import AnalyticalService


ACCOUNT_NUMBER_RE = re.compile(r'^\d{5}$')
SITE_CODE_RE = re.compile(r'^[\d\w]{3}$')
SETUP_CODE = """
    <script type="text/javascript">var _kiq = _kiq || []; %(commands)s</script>
    <script type="text/javascript" src="//s3.amazonaws.com/ki.js/%(account_number)s/%(site_code)s.js" async="true"></script>
"""
IDENTIFY_CODE = "_kiq.push(['identify', '%s']);"
SHOW_SURVEY_CODE = "_kiq.push(['showSurvey', %s]);"
SHOW_SURVEY_CONTEXT_KEY = 'kiss_insights_show_survey'

class KissInsightsService(AnalyticalService):
    def __init__(self):
        self.account_number = self.get_required_setting(
                'KISS_INSIGHTS_ACCOUNT_NUMBER', ACCOUNT_NUMBER_RE,
                "must be a string containing an five-digit number")
        self.site_code = self.get_required_setting('KISS_INSIGHTS_SITE_CODE',
                SITE_CODE_RE, "must be a string containing three characters")

    def render_body_top(self, context):
        commands = []
        identity = self.get_identity(context)
        if identity is not None:
            commands.append(IDENTIFY_CODE % identity)
        try:
            commands.append(SHOW_SURVEY_CODE
                    % context[SHOW_SURVEY_CONTEXT_KEY])
        except KeyError:
            pass
        return SETUP_CODE % {'account_number': self.account_number,
                'site_code': self.site_code, 'commands': " ".join(commands)}

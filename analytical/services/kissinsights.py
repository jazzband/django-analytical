"""
KISSinsights service.
"""

import re

from analytical.services.base import AnalyticalService


ACCOUNT_NUMBER_RE = re.compile(r'^\d{5}$')
SITE_CODE_RE = re.compile(r'^[\d\w]{3}$')
TRACKING_CODE = """
    <script type="text/javascript">var _kiq = _kiq || [];</script>
    <script type="text/javascript" src="//s3.amazonaws.com/ki.js/%(account_number)s/%(site_code)s.js" async="true"></script>
"""


class KissInsightsService(AnalyticalService):
    KEY = 'kissinsights'

    def __init__(self):
        self.account_number = self.get_required_setting(
                'KISSINSIGHTS_ACCOUNT_NUMBER', ACCOUNT_NUMBER_RE,
                "must be a string containing an five-digit number")
        self.site_code = self.get_required_setting('KISSINSIGHTS_SITE_CODE',
                SITE_CODE_RE, "must be a string containing three characters")

    def render_body_top(self, context):
        return TRACKING_CODE % {'account_number': self.account_number,
                'site_code': self.site_code}

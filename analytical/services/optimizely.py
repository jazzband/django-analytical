"""
Optimizely service.
"""

import re

from analytical.services.base import AnalyticalService


ACCOUNT_NUMBER_RE = re.compile(r'^\d{7}$')
TRACKING_CODE = """<script src="//cdn.optimizely.com/js/%(account_number)s.js"></script>"""


class OptimizelyService(AnalyticalService):
    KEY = 'optimizely'

    def __init__(self):
        self.account_number = self.get_required_setting(
                'OPTIMIZELY_ACCOUNT_NUMBER', ACCOUNT_NUMBER_RE,
                "must be a string containing an seven-digit number")

    def render_head_top(self, context):
        return TRACKING_CODE % {'account_number': self.account_number}

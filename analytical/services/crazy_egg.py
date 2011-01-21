"""
Crazy Egg service.
"""

import re

from analytical.services.base import AnalyticalService


ACCOUNT_NUMBER_RE = re.compile(r'^\d{8}$')
TRACK_CODE = """<script type="text/javascript" src="//dnn506yrbagrg.cloudfront.net/pages/scripts/%(account_nr_1)s/%(account_nr_2)s.js"</script>"""


class CrazyEggService(AnalyticalService):
    KEY = 'crazy_egg'

    def __init__(self):
        self.account_nr = self.get_required_setting('CRAZY_EGG_ACCOUNT_NUMBER',
                ACCOUNT_NUMBER_RE,
                "must be a string containing an eight-digit number")

    def render_body_bottom(self, context):
        return TRACK_CODE % {'account_nr_1': self.account_nr[:4],
            'account_nr_2': self.account_nr[4:]}

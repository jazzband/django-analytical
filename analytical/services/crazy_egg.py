"""
Crazy Egg service.
"""

import re

from analytical.services.base import AnalyticalService


ACCOUNT_NUMBER_RE = re.compile(r'^\d{8}$')
SETUP_CODE = """<script type="text/javascript" src="//dnn506yrbagrg.cloudfront.net/pages/scripts/%(account_nr_1)s/%(account_nr_2)s.js"</script>"""
USERVAR_CODE = "CE2.set(%(varnr)d, '%(value)s');"
USERVAR_CONTEXT_VAR = 'crazy_egg_uservars'


class CrazyEggService(AnalyticalService):
    def __init__(self):
        self.account_nr = self.get_required_setting('CRAZY_EGG_ACCOUNT_NUMBER',
                ACCOUNT_NUMBER_RE,
                "must be a string containing an eight-digit number")

    def render_body_bottom(self, context):
        html = SETUP_CODE % {'account_nr_1': self.account_nr[:4],
            'account_nr_2': self.account_nr[4:]}
        uservars = context.get(USERVAR_CONTEXT_VAR, {})
        if uservars:
            js = "".join(USERVAR_CODE % {'varnr': varnr, 'value': value}
                        for (varnr, value) in uservars.items())
            html = '%s\n<script type="text/javascript">%s</script>' \
                    % (html, js)
        return html

"""
KISSinsights template tags.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import get_identity, get_required_setting


ACCOUNT_NUMBER_RE = re.compile(r'^\d+$')
SITE_CODE_RE = re.compile(r'^[\w]+$')
SETUP_CODE = """
    <script type="text/javascript">var _kiq = _kiq || []; %(commands)s</script>
    <script type="text/javascript" src="//s3.amazonaws.com/ki.js/%(account_number)s/%(site_code)s.js" async="true"></script>
"""
IDENTIFY_CODE = "_kiq.push(['identify', '%s']);"
SHOW_SURVEY_CODE = "_kiq.push(['showSurvey', %s]);"
SHOW_SURVEY_CONTEXT_KEY = 'kiss_insights_show_survey'


register = Library()


@register.tag
def kiss_insights(parser, token):
    """
    KISSinsights set-up template tag.

    Renders Javascript code to set-up surveys.  You must supply
    your account number and site code in the
    ``KISS_INSIGHTS_ACCOUNT_NUMBER`` and ``KISS_INSIGHTS_SITE_CODE``
    settings.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return KissInsightsNode()

class KissInsightsNode(Node):
    def __init__(self):
        self.account_number = get_required_setting(
                'KISS_INSIGHTS_ACCOUNT_NUMBER', ACCOUNT_NUMBER_RE,
                "must be (a string containing) a number")
        self.site_code = get_required_setting('KISS_INSIGHTS_SITE_CODE',
                SITE_CODE_RE, "must be a string containing three characters")

    def render(self, context):
        commands = []
        identity = get_identity(context, 'kiss_insights')
        if identity is not None:
            commands.append(IDENTIFY_CODE % identity)
        try:
            commands.append(SHOW_SURVEY_CODE
                    % context[SHOW_SURVEY_CONTEXT_KEY])
        except KeyError:
            pass
        html = SETUP_CODE % {'account_number': self.account_number,
                'site_code': self.site_code, 'commands': " ".join(commands)}
        return html


def contribute_to_analytical(add_node):
    KissInsightsNode()  # ensure properly configured
    add_node('body_top', KissInsightsNode)

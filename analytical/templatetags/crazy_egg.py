"""
Crazy Egg template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import is_internal_ip, disable_html, get_required_setting


ACCOUNT_NUMBER_RE = re.compile(r'^\d+$')
SETUP_CODE = """<script type="text/javascript" src="//dnn506yrbagrg.cloudfront.net/pages/scripts/%(account_nr_1)s/%(account_nr_2)s.js"></script>"""
USERVAR_CODE = "CE2.set(%(varnr)d, '%(value)s');"


register = Library()


@register.tag
def crazy_egg(parser, token):
    """
    Crazy Egg tracking template tag.

    Renders Javascript code to track page clicks.  You must supply
    your Crazy Egg account number (as a string) in the
    ``CRAZY_EGG_ACCOUNT_NUMBER`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return CrazyEggNode()

class CrazyEggNode(Node):
    def __init__(self):
        self.account_nr = get_required_setting('CRAZY_EGG_ACCOUNT_NUMBER',
                ACCOUNT_NUMBER_RE, "must be (a string containing) a number")

    def render(self, context):
        html = SETUP_CODE % {'account_nr_1': self.account_nr[:4],
            'account_nr_2': self.account_nr[4:]}
        values = (context.get('crazy_egg_var%d' % i) for i in range(1, 6))
        vars = [(i, v) for i, v in enumerate(values, 1) if v is not None]
        if vars:
            js = " ".join(USERVAR_CODE % {'varnr': varnr, 'value': value}
                        for (varnr, value) in vars)
            html = '%s\n<script type="text/javascript">%s</script>' \
                    % (html, js)
        if is_internal_ip(context, 'CRAZY_EGG'):
            html = disable_html(html, 'Crazy Egg')
        return html


def contribute_to_analytical(add_node):
    CrazyEggNode()  # ensure properly configured
    add_node('body_bottom', CrazyEggNode)

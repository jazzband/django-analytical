"""
Contentsquare template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

CONTENTSQUARE_TRACKING_CODE = """\
<script>
    (function (c, s, q, u, a, r, e) {
        c.hj=c.hj||function(){(c.hj.q=c.hj.q||[]).push(arguments)};
        c._hjSettings = { hjid: a };
        r = s.getElementsByTagName('head')[0];
        e = s.createElement('script');
        e.async = true;
        e.src = q + c._hjSettings.hjid + u;
        r.appendChild(e);
    })(window, document, 'https://static.hj.contentsquare.net/c/csq-', '.js', %(CONTENTSQUARE_SITE_ID)s);
</script>
"""

register = Library()


def _validate_no_args(token):
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])


@register.tag
def contentsquare(parser, token):
    """
    Contentsquare template tag.
    """
    _validate_no_args(token)
    return ContentsquareNode()


class ContentsquareNode(Node):

    def __init__(self):
        self.site_id = get_required_setting(
            'CONTENTSQUARE_SITE_ID',
            re.compile(r'^\d+$'),
            "must be (a string containing) a number",
        )

    def render(self, context):
        html = CONTENTSQUARE_TRACKING_CODE % {'CONTENTSQUARE_SITE_ID': self.site_id}
        if is_internal_ip(context, 'CONTENTSQUARE'):
            return disable_html(html, 'Contentsquare')
        else:
            return html


def contribute_to_analytical(add_node):
    # ensure properly configured
    ContentsquareNode()
    add_node('head_bottom', ContentsquareNode)

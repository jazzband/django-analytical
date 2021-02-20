"""
Lucky Orange template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

LUCKYORANGE_TRACKING_CODE = """\
<script type='text/javascript'>
window.__lo_site_id = %(LUCKYORANGE_SITE_ID)s;
(function() {
    var wa = document.createElement('script'); wa.type = 'text/javascript'; wa.async = true;
    wa.src = 'https://d10lpsik1i8c69.cloudfront.net/w.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(wa, s);
})();
</script>
"""


register = Library()


def _validate_no_args(token):
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])


@register.tag
def luckyorange(parser, token):
    """
    Lucky Orange template tag.
    """
    _validate_no_args(token)
    return LuckyOrangeNode()


class LuckyOrangeNode(Node):

    def __init__(self):
        self.site_id = get_required_setting(
            'LUCKYORANGE_SITE_ID',
            re.compile(r'^\d+$'),
            "must be (a string containing) a number",
        )

    def render(self, context):
        html = LUCKYORANGE_TRACKING_CODE % {'LUCKYORANGE_SITE_ID': self.site_id}
        if is_internal_ip(context, 'LUCKYORANGE'):
            return disable_html(html, 'Lucky Orange')
        else:
            return html


def contribute_to_analytical(add_node):
    # ensure properly configured
    LuckyOrangeNode()
    add_node('head_bottom', LuckyOrangeNode)

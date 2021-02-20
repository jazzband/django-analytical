"""
Hotjar template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

HOTJAR_TRACKING_CODE = """\
<script>
(function(h,o,t,j,a,r){
    h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
    h._hjSettings={hjid:%(HOTJAR_SITE_ID)s,hjsv:6};
    a=o.getElementsByTagName('head')[0];
    r=o.createElement('script');r.async=1;
    r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
    a.appendChild(r);
})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""


register = Library()


def _validate_no_args(token):
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])


@register.tag
def hotjar(parser, token):
    """
    Hotjar template tag.
    """
    _validate_no_args(token)
    return HotjarNode()


class HotjarNode(Node):

    def __init__(self):
        self.site_id = get_required_setting(
            'HOTJAR_SITE_ID',
            re.compile(r'^\d+$'),
            "must be (a string containing) a number",
        )

    def render(self, context):
        html = HOTJAR_TRACKING_CODE % {'HOTJAR_SITE_ID': self.site_id}
        if is_internal_ip(context, 'HOTJAR'):
            return disable_html(html, 'Hotjar')
        else:
            return html


def contribute_to_analytical(add_node):
    # ensure properly configured
    HotjarNode()
    add_node('head_bottom', HotjarNode)

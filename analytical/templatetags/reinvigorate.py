"""
Reinvigorate template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_identity, is_internal_ip, disable_html, \
        get_required_setting


TRACKING_ID_RE = re.compile(r'^[\w\d]+-[\w\d]+$')
TRACKING_CODE = """
    <script type="text/javascript">
      document.write(unescape("%%3Cscript src='" + (("https:" == document.location.protocol) ? "https://ssl-" : "http://") + "include.reinvigorate.net/re_.js' type='text/javascript'%%3E%%3C/script%%3E"));
    </script>
    <script type="text/javascript">
      try {
        %(tags)s
        reinvigorate.track("%(tracking_id)s");
      } catch(err) {}
    </script>
"""


register = Library()


@register.tag
def reinvigorate(parser, token):
    """
    Reinvigorate tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Reinvigorate tracking ID (as a string) in the
    ``REINVIGORATE_TRACKING_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ReinvigorateNode()

class ReinvigorateNode(Node):
    def __init__(self):
        self.tracking_id = get_required_setting('REINVIGORATE_TRACKING_ID',
                TRACKING_ID_RE,
                "must be a string looking like XXXXX-XXXXXXXXXX")

    def render(self, context):
        re_vars = {}
        for dict_ in context:
            for var, val in dict_.items():
                if var.startswith('reinvigorate_'):
                    re_vars[var[13:]] = val
        if 'name' not in re_vars:
            identity = get_identity(context, 'reinvigorate',
                    lambda u: u.get_full_name())
            if identity is not None:
                re_vars['name'] = identity
        if 'context' not in re_vars:
            email = get_identity(context, 'reinvigorate', lambda u: u.email)
            if email is not None:
                re_vars['context'] = email
        tags = " ".join("var re_%s_tag = %s;" % (tag, simplejson.dumps(value))
                for tag, value in re_vars.items())

        html = TRACKING_CODE % {'tracking_id': self.tracking_id,
                'tags': tags}
        if is_internal_ip(context, 'REINVIGORATE'):
            html = disable_html(html, 'Reinvigorate')
        return html


def contribute_to_analytical(add_node):
    ReinvigorateNode()  # ensure properly configured
    add_node('body_bottom', ReinvigorateNode)

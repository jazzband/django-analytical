"""
Performable template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import is_internal_ip, disable_html, get_identity, \
        get_required_setting


API_KEY_RE = re.compile(r'^\w+$')
SETUP_CODE = """
    <script src="//d1nu2rn22elx8m.cloudfront.net/performable/pax/%(api_key)s.js" type="text/javascript"></script>
"""
IDENTIFY_CODE = """
    <script type="text/javascript">
      var _paq = _paq || [];
      _paq.push(["identify", {identity: "%s"}]);
    </script>
"""
EMBED_CODE = """
    <script type="text/javascript" src="//d1nu2rn22elx8m.cloudfront.net/performable/embed/page.js"></script>
    <script type="text/javascript">
      (function() {
      var $f = new PerformableEmbed();
      $f.initialize({'host': '%(hostname)s', 'page': '%(page_id)s'});
      $f.write();
    })()
    </script>
"""

register = Library()


@register.tag
def performable(parser, token):
    """
    Performable template tag.

    Renders Javascript code to set-up Performable tracking.  You must
    supply your Performable API key in the ``PERFORMABLE_API_KEY``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return PerformableNode()

class PerformableNode(Node):
    def __init__(self):
        self.api_key = get_required_setting('PERFORMABLE_API_KEY', API_KEY_RE,
                "must be a string looking like 'XXXXX'")

    def render(self, context):
        html = SETUP_CODE % {'api_key': self.api_key}
        identity = get_identity(context, 'performable')
        if identity is not None:
            html = "%s%s" % (IDENTIFY_CODE % identity, html)
        if is_internal_ip(context, 'PERFORMABLE'):
            html = disable_html(html, 'Performable')
        return html


@register.simple_tag
def performable_embed(hostname, page_id):
    """
    Include a Performable landing page.
    """
    return EMBED_CODE % {'hostname': hostname, 'page_id': page_id}


def contribute_to_analytical(add_node):
    PerformableNode()  # ensure properly configured
    add_node('body_bottom', PerformableNode)

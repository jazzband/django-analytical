"""
Woopra template tags and filters.
"""

from __future__ import absolute_import

import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_identity, get_user_from_context, \
        is_internal_ip, disable_html, get_required_setting


DOMAIN_RE = re.compile(r'^\S+$')
TRACKING_CODE = """
     <script type="text/javascript">
      var woo_settings = %(settings)s;
      var woo_visitor = %(visitor)s;
      (function(){
        var wsc=document.createElement('script');
        wsc.type='text/javascript';
        wsc.src=document.location.protocol+'//static.woopra.com/js/woopra.js';
        wsc.async=true;
        var ssc = document.getElementsByTagName('script')[0];
        ssc.parentNode.insertBefore(wsc, ssc);
      })();
    </script>
"""


register = Library()


@register.tag
def woopra(parser, token):
    """
    Woopra tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Woopra domain in the ``WOOPRA_DOMAIN`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return WoopraNode()

class WoopraNode(Node):
    def __init__(self):
        self.domain = get_required_setting('WOOPRA_DOMAIN', DOMAIN_RE,
                "must be a domain name")

    def render(self, context):
        settings = self._get_settings(context)
        visitor = self._get_visitor(context)

        html = TRACKING_CODE % {
            'settings': simplejson.dumps(settings),
            'visitor': simplejson.dumps(visitor),
        }
        if is_internal_ip(context, 'WOOPRA'):
            html = disable_html(html, 'Woopra')
        return html

    def _get_settings(self, context):
        vars = {'domain': self.domain}
        try:
            vars['idle_timeout'] = str(settings.WOOPRA_IDLE_TIMEOUT)
        except AttributeError:
            pass
        return vars

    def _get_visitor(self, context):
        vars = {}
        for dict_ in context:
            for var, val in dict_.items():
                if var.startswith('woopra_'):
                    vars[var[7:]] = val
        if 'name' not in vars and 'email' not in vars:
            user = get_user_from_context(context)
            if user is not None and user.is_authenticated():
                vars['name'] = get_identity(context, 'woopra',
                        self._identify, user)
                if user.email:
                    vars['email'] = user.email
        return vars

    def _identify(self, user):
        name = user.get_full_name()
        if not name:
            name = user.username
        return name


def contribute_to_analytical(add_node):
    WoopraNode()  # ensure properly configured
    add_node('head_bottom', WoopraNode)

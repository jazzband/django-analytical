"""
Olark template tags.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_identity, get_required_setting


SITE_ID_RE = re.compile(r'^\d+-\d+-\d+-\d+$')
SETUP_CODE = """
    <script type='text/javascript'>
      /*{literal}<![CDATA[*/ window.olark||(function(k){var g=window,j=document,a=g.location.protocol=="https:"?"https:":"http:",i=k.name,b="load",h="addEventListener";(function(){g[i]=function(){(c.s=c.s||[]).push(arguments)};var c=g[i]._={},f=k.methods.length;while(f--){(function(l){g[i][l]=function(){g[i]("call",l,arguments)}})(k.methods[f])}c.l=k.loader;c.i=arguments.callee;c.p={0:+new Date};c.P=function(l){c.p[l]=new Date-c.p[0]};function e(){c.P(b);g[i](b)}g[h]?g[h](b,e,false):g.attachEvent("on"+b,e);c.P(1);var d=j.createElement("script"),m=document.getElementsByTagName("script")[0];d.type="text/javascript";d.async=true;d.src=a+"//"+c.l;m.parentNode.insertBefore(d,m);c.P(2)})()})({loader:(function(a){return "static.olark.com/jsclient/loader1.js?ts="+(a?a[1]:(+new Date))})(document.cookie.match(/olarkld=([0-9]+)/)),name:"olark",methods:["configure","extend","declare","identify"]}); olark.identify('%(site_id)s');/*]]>{/literal}*/
      %(extra_code)s
    </script>
"""
NICKNAME_CODE = "olark('api.chat.updateVisitorNickname', {snippet: '%s'});"
NICKNAME_CONTEXT_KEY = 'olark_nickname'
STATUS_CODE = "olark('api.chat.updateVisitorStatus', {snippet: %s});"
STATUS_CONTEXT_KEY = 'olark_status'


register = Library()


@register.tag
def olark(parser, token):
    """
    Olark set-up template tag.

    Renders Javascript code to set-up Olark chat.  You must supply
    your site ID in the ``OLARK_SITE_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return OlarkNode()

class OlarkNode(Node):
    def __init__(self):
        self.site_id = get_required_setting('OLARK_SITE_ID', SITE_ID_RE,
                "must be a string looking like 'XXXX-XXX-XX-XXXX'")

    def render(self, context):
        extra_code = []
        try:
            extra_code.append(NICKNAME_CODE % context[NICKNAME_CONTEXT_KEY])
        except KeyError:
            identity = get_identity(context, 'olark', self._get_nickname)
            if identity is not None:
                extra_code.append(NICKNAME_CODE % identity)
        try:
            extra_code.append(STATUS_CODE %
                    simplejson.dumps(context[STATUS_CONTEXT_KEY]))
        except KeyError:
            pass
        html = SETUP_CODE % {'site_id': self.site_id,
                'extra_code': " ".join(extra_code)}
        return html

    def _get_nickname(self, user):
        name = user.get_full_name()
        if name:
            return "%s (%s)" % (name, user.username)
        else:
            return user.username


def contribute_to_analytical(add_node):
    OlarkNode()  # ensure properly configured
    add_node('body_bottom', OlarkNode)

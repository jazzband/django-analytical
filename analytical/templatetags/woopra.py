"""
Woopra template tags and filters.
"""

from __future__ import absolute_import

import json
import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    get_user_from_context,
    is_internal_ip,
)

DOMAIN_RE = re.compile(r'^\S+$')
TRACKING_CODE = """
     <script type="text/javascript">
      var woo_settings = %(settings)s;
      var woo_visitor = %(visitor)s;
      !function(){var a,b,c,d=window,e=document,f=arguments,g="script",h=["config","track","trackForm","trackClick","identify","visit","push","call"],i=function(){var a,b=this,c=function(a){b[a]=function(){return b._e.push([a].concat(Array.prototype.slice.call(arguments,0))),b}};for(b._e=[],a=0;a<h.length;a++)c(h[a])};for(d.__woo=d.__woo||{},a=0;a<f.length;a++)d.__woo[f[a]]=d[f[a]]=d[f[a]]||new i;b=e.createElement(g),b.async=1,b.src="//static.woopra.com/js/w.js",c=e.getElementsByTagName(g)[0],c.parentNode.insertBefore(b,c)}("woopra");
      woopra.config(woo_settings);
      woopra.identify(woo_visitor);
      woopra.track();
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
        self.domain = get_required_setting(
            'WOOPRA_DOMAIN', DOMAIN_RE,
            "must be a domain name")

    def render(self, context):
        settings = self._get_settings(context)
        visitor = self._get_visitor(context)

        html = TRACKING_CODE % {
            'settings': json.dumps(settings, sort_keys=True),
            'visitor': json.dumps(visitor, sort_keys=True),
        }
        if is_internal_ip(context, 'WOOPRA'):
            html = disable_html(html, 'Woopra')
        return html

    def _get_settings(self, context):
        variables = {'domain': self.domain}
        try:
            variables['idle_timeout'] = str(settings.WOOPRA_IDLE_TIMEOUT)
        except AttributeError:
            pass
        try:
            variables['cookie_name'] = str(settings.WOOPRA_COOKIE_NAME)
        except AttributeError:
            pass
        try:
            variables['cookie_domain'] = str(settings.WOOPRA_COOKIE_DOMAIN)
        except AttributeError:
            pass
        try:
            variables['cookie_path'] = str(settings.WOOPRA_COOKIE_PATH)
        except AttributeError:
            pass
        try:
            variables['cookie_expire'] = str(settings.WOOPRA_COOKIE_EXPIRE)
        except AttributeError:
            pass
        try:
            variables['ping'] = str(settings.WOOPRA_PING)
        except AttributeError:
            pass
        try:
            variables['ping_interval'] = str(settings.WOOPRA_PING_INTERVAL)
        except AttributeError:
            pass
        try:
            variables['download_tracking'] = str(settings.WOOPRA_DOWNLOAD_TRACKING)
        except AttributeError:
            pass
        try:
            variables['outgoing_tracking'] = str(settings.WOOPRA_OUTGOING_TRACKING)
        except AttributeError:
            pass
        try:
            variables['outgoing_ignore_subdomain'] = str(settings.WOOPRA_OUTGOING_IGNORE_SUBDOMAIN)
        except AttributeError:
            pass
        try:
            variables['download_pause'] = str(settings.WOOPRA_DOWNLOAD_PAUSE)
        except AttributeError:
            pass
        try:
            variables['outgoing_pause'] = str(settings.WOOPRA_OUTGOING_PAUSE)
        except AttributeError:
            pass
        try:
            variables['ignore_query_url'] = str(settings.WOOPRA_IGNORE_QUERY_URL)
        except AttributeError:
            pass
        try:
            variables['map_query_params'] = str(settings.WOOPRA_MAP_QUERY_PARAMS)
        except AttributeError:
            pass
        try:
            variables['hide_campaign'] = str(settings.WOOPRA_HIDE_CAMPAIGN)
        except AttributeError:
            pass
            
        return variables

    def _get_visitor(self, context):
        params = {}
        for dict_ in context:
            for var, val in dict_.items():
                if var.startswith('woopra_'):
                    params[var[7:]] = val
        if 'name' not in params and 'email' not in params:
            user = get_user_from_context(context)
            if user is not None and user.is_authenticated():
                params['name'] = get_identity(
                    context, 'woopra', self._identify, user)
                if user.email:
                    params['email'] = user.email
        return params

    def _identify(self, user):
        name = user.get_full_name()
        if not name:
            name = user.username
        return name


def contribute_to_analytical(add_node):
    WoopraNode()  # ensure properly configured
    add_node('head_bottom', WoopraNode)

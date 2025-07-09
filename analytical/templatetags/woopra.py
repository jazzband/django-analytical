"""
Woopra template tags and filters.
"""

import json
import re
from contextlib import suppress

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    AnalyticalException,
    disable_html,
    get_identity,
    get_required_setting,
    get_user_from_context,
    get_user_is_authenticated,
    is_internal_ip,
)

DOMAIN_RE = re.compile(r'^\S+$')
TRACKING_CODE = """
     <script>
      var woo_settings = %(settings)s;
      var woo_visitor = %(visitor)s;
      !function(){var a,b,c,d=window,e=document,f=arguments,g="script",h=["config","track","trackForm","trackClick","identify","visit","push","call"],i=function(){var a,b=this,c=function(a){b[a]=function(){return b._e.push([a].concat(Array.prototype.slice.call(arguments,0))),b}};for(b._e=[],a=0;a<h.length;a++)c(h[a])};for(d.__woo=d.__woo||{},a=0;a<f.length;a++)d.__woo[f[a]]=d[f[a]]=d[f[a]]||new i;b=e.createElement(g),b.async=1,b.src="//static.woopra.com/js/w.js",c=e.getElementsByTagName(g)[0],c.parentNode.insertBefore(b,c)}("woopra");
      woopra.config(woo_settings);
      woopra.identify(woo_visitor);
      woopra.track();
    </script>
"""  # noqa

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
            'WOOPRA_DOMAIN', DOMAIN_RE, 'must be a domain name'
        )

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
        woopra_int_settings = {
            'idle_timeout': 'WOOPRA_IDLE_TIMEOUT',
        }
        woopra_str_settings = {
            'cookie_name': 'WOOPRA_COOKIE_NAME',
            'cookie_domain': 'WOOPRA_COOKIE_DOMAIN',
            'cookie_path': 'WOOPRA_COOKIE_PATH',
            'cookie_expire': 'WOOPRA_COOKIE_EXPIRE',
        }
        woopra_bool_settings = {
            'click_tracking': 'WOOPRA_CLICK_TRACKING',
            'download_tracking': 'WOOPRA_DOWNLOAD_TRACKING',
            'outgoing_tracking': 'WOOPRA_OUTGOING_TRACKING',
            'outgoing_ignore_subdomain': 'WOOPRA_OUTGOING_IGNORE_SUBDOMAIN',
            'ignore_query_url': 'WOOPRA_IGNORE_QUERY_URL',
            'hide_campaign': 'WOOPRA_HIDE_CAMPAIGN',
        }

        for key, name in woopra_int_settings.items():
            with suppress(AttributeError):
                variables[key] = getattr(settings, name)
                if type(variables[key]) is not int:
                    raise AnalyticalException(f'{name} must be an int value')

        for key, name in woopra_str_settings.items():
            with suppress(AttributeError):
                variables[key] = getattr(settings, name)
                if type(variables[key]) is not str:
                    raise AnalyticalException(f'{name} must be a string value')

        for key, name in woopra_bool_settings.items():
            with suppress(AttributeError):
                variables[key] = getattr(settings, name)
                if type(variables[key]) is not bool:
                    raise AnalyticalException(f'{name} must be a boolean value')

        return variables

    def _get_visitor(self, context):
        params = {}
        for dict_ in context:
            for var, val in dict_.items():
                if var.startswith('woopra_'):
                    params[var[7:]] = val
        if 'name' not in params and 'email' not in params:
            user = get_user_from_context(context)
            if user is not None and get_user_is_authenticated(user):
                params['name'] = get_identity(context, 'woopra', self._identify, user)
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

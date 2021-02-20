"""
Mixpanel template tags and filters.
"""

import json
import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    is_internal_ip,
)

MIXPANEL_API_TOKEN_RE = re.compile(r'^[0-9a-f]{32}$')
TRACKING_CODE = """
    <script type="text/javascript">(function(e,b){if(!b.__SV){var a,f,i,g;window.mixpanel=b;a=e.createElement("script");a.type="text/javascript";a.async=!0;a.src=("https:"===e.location.protocol?"https:":"http:")+'//cdn.mxpnl.com/libs/mixpanel-2.2.min.js';f=e.getElementsByTagName("script")[0];f.parentNode.insertBefore(a,f);b._i=[];b.init=function(a,e,d){function f(b,h){var a=h.split(".");2==a.length&&(b=b[a[0]],h=a[1]);b[h]=function(){b.push([h].concat(Array.prototype.slice.call(arguments,0)))}}var c=b;"undefined"!==
typeof d?c=b[d]=[]:d="mixpanel";c.people=c.people||[];c.toString=function(b){var a="mixpanel";"mixpanel"!==d&&(a+="."+d);b||(a+=" (stub)");return a};c.people.toString=function(){return c.toString(1)+".people (stub)"};i="disable track track_pageview track_links track_forms register register_once alias unregister identify name_tag set_config people.set people.increment people.append people.track_charge people.clear_charges people.delete_user".split(" ");for(g=0;g<i.length;g++)f(c,i[g]);b._i.push([a,
e,d])};b.__SV=1.2}})(document,window.mixpanel||[]);
    mixpanel.init('%(token)s');
    %(commands)s
    </script>
"""  # noqa
IDENTIFY_CODE = "mixpanel.identify('%s');"
IDENTIFY_PROPERTIES = "mixpanel.people.set(%s);"
EVENT_CODE = "mixpanel.track('%(name)s', %(properties)s);"
EVENT_CONTEXT_KEY = 'mixpanel_event'

register = Library()


@register.tag
def mixpanel(parser, token):
    """
    Mixpanel tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Mixpanel token in the ``MIXPANEL_API_TOKEN`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return MixpanelNode()


class MixpanelNode(Node):
    def __init__(self):
        self._token = get_required_setting(
                'MIXPANEL_API_TOKEN', MIXPANEL_API_TOKEN_RE,
                "must be a string containing a 32-digit hexadecimal number")

    def render(self, context):
        commands = []
        identity = get_identity(context, 'mixpanel')
        if identity is not None:
            if isinstance(identity, dict):
                commands.append(IDENTIFY_CODE % identity.get('id', identity.get('username')))
                commands.append(IDENTIFY_PROPERTIES % json.dumps(identity, sort_keys=True))
            else:
                commands.append(IDENTIFY_CODE % identity)
        try:
            name, properties = context[EVENT_CONTEXT_KEY]
            commands.append(EVENT_CODE % {
                'name': name,
                'properties': json.dumps(properties, sort_keys=True),
            })
        except KeyError:
            pass
        html = TRACKING_CODE % {
            'token': self._token,
            'commands': " ".join(commands),
        }
        if is_internal_ip(context, 'MIXPANEL'):
            html = disable_html(html, 'Mixpanel')
        return mark_safe(html)


def contribute_to_analytical(add_node):
    MixpanelNode()  # ensure properly configured
    add_node('head_bottom', MixpanelNode)

"""
intercom.io template tags and filters.
"""

from __future__ import absolute_import
import json
import time
import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, \
        is_internal_ip, get_user_from_context, get_identity

APP_ID_RE = re.compile(r'[\da-f]+$')
TRACKING_CODE = """
<script id="IntercomSettingsScriptTag">
  window.intercomSettings = %(settings_json)s;
</script>
<script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',intercomSettings);}else{var d=document;var i=function(){i.c(arguments)};i.q=[];i.c=function(args){i.q.push(args)};w.Intercom=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://static.intercomcdn.com/intercom.v1.js';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})()</script>
"""

register = Library()


@register.tag
def intercom(parser, token):
    """
    Intercom.io template tag.

    Renders Javascript code to intercom.io testing.  You must supply
    your APP ID account number in the ``INTERCOM_APP_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return IntercomNode()


class IntercomNode(Node):
    def __init__(self):
        self.app_id = get_required_setting(
                'INTERCOM_APP_ID', APP_ID_RE,
                "must be a string looking like 'XXXXXXX'")

    def _identify(self, user):
        name = user.get_full_name()
        if not name:
            name = user.username
        return name

    def _get_custom_attrs(self, context):
        params = {}
        for dict_ in context:
            for var, val in dict_.items():
                if var.startswith('intercom_'):
                    params[var[9:]] = val

        user = get_user_from_context(context)
        if user is not None and user.is_authenticated():
            if 'name' not in params:
                params['name'] = get_identity(
                        context, 'intercom', self._identify, user)
            if 'email' not in params and user.email:
                params['email'] = user.email

            params['created_at'] = int(time.mktime(
                    user.date_joined.timetuple()))
        else:
            params['created_at'] = None

        return params

    def render(self, context):
        user = get_user_from_context(context)
        params = self._get_custom_attrs(context)
        params["app_id"] = self.app_id
        html = TRACKING_CODE % {
            "settings_json": json.dumps(params, sort_keys=True)
        }

        if is_internal_ip(context, 'INTERCOM') \
                or not user or not user.is_authenticated():
            # Intercom is disabled for non-logged in users.
            html = disable_html(html, 'Intercom')
        return html


def contribute_to_analytical(add_node):
    IntercomNode()
    add_node('body_bottom', IntercomNode)

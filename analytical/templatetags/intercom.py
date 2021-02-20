"""
intercom.io template tags and filters.
"""

import hashlib
import hmac
import json
import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    get_user_from_context,
    get_user_is_authenticated,
    is_internal_ip,
)

APP_ID_RE = re.compile(r'[\da-z]+$')
TRACKING_CODE = """
<script id="IntercomSettingsScriptTag">
  window.intercomSettings = %(settings_json)s;
</script>
<script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',intercomSettings);}else{var d=document;var i=function(){i.c(arguments)};i.q=[];i.c=function(args){i.q.push(args)};w.Intercom=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://static.intercomcdn.com/intercom.v1.js';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})()</script>
"""  # noqa

register = Library()


def _hashable_bytes(data):
    """
    Coerce strings to hashable bytes.
    """
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return data.encode('ascii')  # Fail on anything non-ASCII.
    else:
        raise TypeError(data)


def intercom_user_hash(data):
    """
    Return a SHA-256 HMAC `user_hash` as expected by Intercom, if configured.

    Return None if the `INTERCOM_HMAC_SECRET_KEY` setting is not configured.
    """
    if getattr(settings, 'INTERCOM_HMAC_SECRET_KEY', None):
        return hmac.new(
            key=_hashable_bytes(settings.INTERCOM_HMAC_SECRET_KEY),
            msg=_hashable_bytes(data),
            digestmod=hashlib.sha256,
        ).hexdigest()
    else:
        return None


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
        if user is not None and get_user_is_authenticated(user):
            if 'name' not in params:
                params['name'] = get_identity(
                        context, 'intercom', self._identify, user)
            if 'email' not in params and user.email:
                params['email'] = user.email

            params.setdefault('user_id', user.pk)

            params['created_at'] = int(user.date_joined.timestamp())
        else:
            params['created_at'] = None

        # Generate a user_hash HMAC to verify the user's identity, if configured.
        # (If both user_id and email are present, the user_id field takes precedence.)
        # See:
        # https://www.intercom.com/help/configure-intercom-for-your-product-or-site/staying-secure/enable-identity-verification-on-your-web-product
        user_hash_data = params.get('user_id', params.get('email'))
        if user_hash_data:
            user_hash = intercom_user_hash(str(user_hash_data))
            if user_hash is not None:
                params.setdefault('user_hash', user_hash)

        return params

    def render(self, context):
        params = self._get_custom_attrs(context)
        params["app_id"] = self.app_id
        html = TRACKING_CODE % {
            "settings_json": json.dumps(params, sort_keys=True)
        }

        if is_internal_ip(context, 'INTERCOM'):
            html = disable_html(html, 'Intercom')
        return html


def contribute_to_analytical(add_node):
    IntercomNode()
    add_node('body_bottom', IntercomNode)

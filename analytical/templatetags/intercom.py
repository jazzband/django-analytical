"""
intercom.io template tags and filters.
"""

from __future__ import absolute_import
import time
import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, get_user_from_context

APP_ID_RE = re.compile(r'[\da-f]+$')
TRACKING_CODE = """
<script id="IntercomSettingsScriptTag">
  window.intercomSettings = {'app_id': '%(app_id)s', 'full_name': '%(full_name)s', 'email': '%(email)s', 'created_at': %(created_at)s};
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

    def render(self, context):
        html = ""
        user = get_user_from_context(context)
        if user is not None and user.is_authenticated():
            html = TRACKING_CODE % {
                'app_id': self.app_id,
                'full_name': "%s %s" % (user.first_name, user.last_name),
                'email': user.email,
                'created_at': int(time.mktime(user.date_joined.timetuple())),
            }
        else:
            # Intercom is disabled for non-logged in users.
            html = disable_html(html, 'Intercom')
        return html


def contribute_to_analytical(add_node):
    IntercomNode()
    add_node('body_bottom', IntercomNode)

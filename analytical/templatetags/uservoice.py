"""
UserVoice template tags.
"""

import json
import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import get_identity, get_required_setting

WIDGET_KEY_RE = re.compile(r'^[a-zA-Z0-9]*$')
TRACKING_CODE = """
    <script type="text/javascript">

    UserVoice=window.UserVoice||[];(function(){
            var uv=document.createElement('script');uv.type='text/javascript';
            uv.async=true;uv.src='//widget.uservoice.com/%(widget_key)s.js';
            var s=document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(uv,s)})();

    UserVoice.push(['set', %(options)s]);
    %(trigger)s
    %(identity)s
    </script>
"""
IDENTITY = """UserVoice.push(['identify', %(options)s]);"""
TRIGGER = "UserVoice.push(['addTrigger', {}]);"
register = Library()


@register.tag
def uservoice(parser, token):
    """
    UserVoice tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your UserVoice Widget Key in the ``USERVOICE_WIDGET_KEY``
    setting or the ``uservoice_widget_key`` template context variable.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return UserVoiceNode()


class UserVoiceNode(Node):
    def __init__(self):
        self.default_widget_key = get_required_setting(
            'USERVOICE_WIDGET_KEY', WIDGET_KEY_RE, "must be an alphanumeric string")

    def render(self, context):
        widget_key = context.get('uservoice_widget_key')
        if not widget_key:
            widget_key = self.default_widget_key
        if not widget_key:
            return ''
        # default
        options = {}
        options.update(getattr(settings, 'USERVOICE_WIDGET_OPTIONS', {}))
        options.update(context.get('uservoice_widget_options', {}))

        identity = get_identity(context, 'uservoice', self._identify)
        if identity:
            identity = IDENTITY % {'options': json.dumps(identity, sort_keys=True)}

        trigger = context.get('uservoice_add_trigger',
                              getattr(settings, 'USERVOICE_ADD_TRIGGER', True))

        html = TRACKING_CODE % {'widget_key': widget_key,
                                'options':  json.dumps(options, sort_keys=True),
                                'trigger': TRIGGER if trigger else '',
                                'identity': identity if identity else ''}
        return html

    def _identify(self, user):
        name = user.get_full_name()
        if not name:
            name = user.username
        return {'name': name, 'email': user.email}


def contribute_to_analytical(add_node):
    UserVoiceNode()  # ensure properly configured
    add_node('body_bottom', UserVoiceNode)

"""
UserVoice template tags.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.utils import simplejson

from analytical.utils import get_identity, get_required_setting


WIDGET_KEY_RE = re.compile(r'^[a-zA-Z0-9]*$')
TRACKING_CODE = """
    <script type="text/javascript">
      var uvOptions = %(options)s;
      (function() {
        var uv = document.createElement('script'); uv.type = 'text/javascript'; uv.async = true;
        uv.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'widget.uservoice.com/%(widget_key)s.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(uv, s);
      })();
    </script>
"""
LINK_CODE = "UserVoice.showPopupWidget(%s);"


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
        self.default_widget_key = get_required_setting('USERVOICE_WIDGET_KEY',
                WIDGET_KEY_RE, "must be an alphanumeric string")

    def render(self, context):
        widget_key = context.get('uservoice_widget_key')
        if not widget_key:
            widget_key = self.default_widget_key
        if not widget_key:
            return ''
        options = {}
        options['enabled'] = context.get('uservoice_show_tab', True)
        options['custom_fields'] = context.get('uservoice_fields', {})
        identity = get_identity(context, 'uservoice')
        if identity is not None:
            # Enable SSO
            pass
        html = TRACKING_CODE % {'widget_key': widget_key,
                'options': simplejson.dumps(options)}
        return html


@register.tag
def uservoice_popup(parser, token):
    """
    UserVoice widget popup template tag.

    Renders the Javascript code to pop-up the UserVoice widget.  For example::

        <a href="#" onclick="{% uservoice_popup %}; return false;">Feedback</a>

    The tag accepts an optional argument specifying the key of the widget you
    want to show::

        <a href="#" onclick="{% uservoice_popup 'XXXXXXXXXXXXXXXXXXXX' %}; return false;">Helpdesk</a>

    If you add this tag without a widget key, the default feedback tab will be
    hidden.
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return UserVoiceLinkNode()
    if len(bits) == 2:
        return UserVoiceKeyLinkNode(bits[1])
    raise TemplateSyntaxError("'%s' takes at most one argument" % bits[0])

class UserVoiceLinkNode(Node):
    def render(self, context):
        context['uservoice_show_tab'] = False
        return LINK_CODE % ''

class UserVoiceKeyLinkNode(Node):
    def __init__(self, widget_key):
        self.widget_key = Variable(widget_key)

    def render(self, context):
        vars = {}
        if self.widget_key:
            vars['widget_key'] = self.widget_key.resolve(context)
        return LINK_CODE % simplejson.dumps(vars)


def contribute_to_analytical(add_node):
    UserVoiceNode()  # ensure properly configured
    add_node('body_bottom', UserVoiceNode)

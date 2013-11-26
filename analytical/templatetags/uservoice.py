"""
UserVoice template tags.
"""

from __future__ import absolute_import

import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_required_setting


WIDGET_KEY_RE = re.compile(r'^[a-zA-Z0-9]*$')
TRACKING_CODE = """
    <script type="text/javascript">

    UserVoice=window.UserVoice||[];(function(){
            var uv=document.createElement('script');uv.type='text/javascript';
            uv.async=true;uv.src='//widget.uservoice.com/%(widget_key)s.js';
            var s=document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(uv,s)})();

    %(options)s
    </script>
"""
OPTION_CODE = """
    UserVoice.push(['%s', %s]);
"""


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
        # default
        options = {'addTrigger': {'mode': 'contact',
                                  'trigger_position': 'bottom-right'}}
        options.update(getattr(settings, 'USERVOICE_WIDGET_OPTIONS', {}))
        options.update(context.get('uservoice_widget_options', {}))

        options = ''.join([OPTION_CODE % (k, simplejson.dumps(v))
                           for k, v in options.iteritems()])

        html = TRACKING_CODE % {'widget_key': widget_key,
                                'options': options}
        return html


def contribute_to_analytical(add_node):
    UserVoiceNode()  # ensure properly configured
    add_node('body_bottom', UserVoiceNode)

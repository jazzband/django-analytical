"""
SnapEngage template tags.
"""

from __future__ import absolute_import

import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError
from django.utils import translation

from analytical.utils import get_identity, get_required_setting


BUTTON_LOCATION_LEFT = 0
BUTTON_LOCATION_RIGHT = 1
BUTTON_LOCATION_TOP = 2
BUTTON_LOCATION_BOTTOM = 3

BUTTON_STYLE_NONE = 0
BUTTON_STYLE_DEFAULT = 1
BUTTON_STYLE_LIVE = 2

FORM_POSITION_TOP_LEFT = 'tl'
FORM_POSITION_TOP_RIGHT = 'tr'
FORM_POSITION_BOTTOM_LEFT = 'bl'
FORM_POSITION_BOTTOM_RIGHT = 'br'

WIDGET_ID_RE = re.compile(r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$')
SETUP_CODE = """
    <script type="text/javascript">
      document.write(unescape("%%3Cscript src='" + ((document.location.protocol=="https:")?"https://snapabug.appspot.com":"http://www.snapengage.com") + "/snapabug.js' type='text/javascript'%%3E%%3C/script%%3E"));</script><script type="text/javascript">
      %(settings_code)s
    </script>
"""
DOMAIN_CODE = 'SnapABug.setDomain("%s");'
SECURE_CONNECTION_CODE = 'SnapABug.setSecureConnexion();'
INIT_CODE = 'SnapABug.init("%s");'
ADDBUTTON_CODE = 'SnapABug.addButton("%(id)s","%(location)s","%(offset)s"%(dynamic_tail)s);'
SETBUTTON_CODE = 'SnapABug.setButton("%s");'
SETEMAIL_CODE = 'SnapABug.setUserEmail("%s"%s);'
SETLOCALE_CODE = 'SnapABug.setLocale("%s");'
FORM_POSITION_CODE = 'SnapABug.setChatFormPosition("%s");'
FORM_TOP_POSITION_CODE = 'SnapABug.setFormTopPosition(%d);'
BUTTONEFFECT_CODE = 'SnapABug.setButtonEffect("%s");'
DISABLE_OFFLINE_CODE = 'SnapABug.allowOffline(false);'
DISABLE_SCREENSHOT_CODE = 'SnapABug.allowScreenshot(false);'
DISABLE_OFFLINE_SCREENSHOT_CODE = 'SnapABug.showScreenshotOption(false);'
DISABLE_PROACTIVE_CHAT_CODE = 'SnapABug.allowProactiveChat(false);'
DISABLE_SOUNDS_CODE = 'SnapABug.allowChatSound(false);'

register = Library()


@register.tag
def snapengage(parser, token):
    """
    SnapEngage set-up template tag.

    Renders Javascript code to set-up SnapEngage chat.  You must supply
    your widget ID in the ``SNAPENGAGE_WIDGET_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return SnapEngageNode()

class SnapEngageNode(Node):
    def __init__(self):
        self.widget_id = get_required_setting('SNAPENGAGE_WIDGET_ID',
                WIDGET_ID_RE, "must be a string looking like this: "
                    "'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'")

    def render(self, context):
        settings_code = []

        domain = self._get_setting(context, 'snapengage_domain',
                'SNAPENGAGE_DOMAIN')
        if domain is not None:
            settings_code.append(DOMAIN_CODE % domain)

        secure_connection = self._get_setting(context,
                'snapengage_secure_connection', 'SNAPENGAGE_SECURE_CONNECTION',
                False)
        if secure_connection:
            settings_code.append(SECURE_CONNECTION_CODE)

        email = context.get('snapengage_email')
        if email is None:
            email = get_identity(context, 'snapengage', lambda u: u.email)
        if email is not None:
            if self._get_setting(context, 'snapengage_readonly_email',
                    'SNAPENGAGE_READONLY_EMAIL', False):
                readonly_tail = ',true'
            else:
                readonly_tail = ''
            settings_code.append(SETEMAIL_CODE % (email, readonly_tail))

        locale = self._get_setting(context, 'snapengage_locale',
                'SNAPENGAGE_LOCALE')
        if locale is None:
            locale = translation.to_locale(translation.get_language())
        settings_code.append(SETLOCALE_CODE % locale)

        form_position = self._get_setting(context,
                'snapengage_form_position', 'SNAPENGAGE_FORM_POSITION')
        if form_position is not None:
            settings_code.append(FORM_POSITION_CODE % form_position)

        form_top_position = self._get_setting(context,
                'snapengage_form_top_position', 'SNAPENGAGE_FORM_TOP_POSITION')
        if form_top_position is not None:
            settings_code.append(FORM_TOP_POSITION_CODE % form_top_position)

        show_offline = self._get_setting(context, 'snapengage_show_offline',
                'SNAPENGAGE_SHOW_OFFLINE', True)
        if not show_offline:
            settings_code.append(DISABLE_OFFLINE_CODE)

        screenshots = self._get_setting(context, 'snapengage_screenshots',
                'SNAPENGAGE_SCREENSHOTS', True)
        if not screenshots:
            settings_code.append(DISABLE_SCREENSHOT_CODE)

        offline_screenshots = self._get_setting(context,
            'snapengage_offline_screenshots',
            'SNAPENGAGE_OFFLINE_SCREENSHOTS', True)
        if not offline_screenshots:
            settings_code.append(DISABLE_OFFLINE_SCREENSHOT_CODE)

        if not context.get('snapengage_proactive_chat', True):
            settings_code.append(DISABLE_PROACTIVE_CHAT_CODE)

        sounds = self._get_setting(context, 'snapengage_sounds',
            'SNAPENGAGE_SOUNDS', True)
        if not sounds:
            settings_code.append(DISABLE_SOUNDS_CODE)

        button_effect = self._get_setting(context, 'snapengage_button_effect',
                'SNAPENGAGE_BUTTON_EFFECT')
        if button_effect is not None:
            settings_code.append(BUTTONEFFECT_CODE % button_effect)

        button = self._get_setting(context, 'snapengage_button',
                'SNAPENGAGE_BUTTON', BUTTON_STYLE_DEFAULT)
        if button == BUTTON_STYLE_NONE:
            settings_code.append(INIT_CODE % self.widget_id)
        else:
            if not isinstance(button, int):
                # Assume button as a URL to a custom image
                settings_code.append(SETBUTTON_CODE % button)
            button_location = self._get_setting(context,
                    'snapengage_button_location', 'SNAPENGAGE_BUTTON_LOCATION',
                    BUTTON_LOCATION_LEFT)
            button_offset = self._get_setting(context,
                    'snapengage_button_location_offset',
                    'SNAPENGAGE_BUTTON_LOCATION_OFFSET', '55%')
            settings_code.append(ADDBUTTON_CODE % {
                'id': self.widget_id,
                'location': button_location,
                'offset': button_offset,
                'dynamic_tail': ',true' if (button == BUTTON_STYLE_LIVE) else '',
                })
        html = SETUP_CODE % {'widget_id': self.widget_id,
                'settings_code': " ".join(settings_code)}
        return html

    def _get_setting(self, context, context_key, setting=None, default=None):
        try:
            return context[context_key]
        except KeyError:
            if setting is not None:
                return getattr(settings, setting, default)
            else:
                return default


def contribute_to_analytical(add_node):
    SnapEngageNode()  # ensure properly configured
    add_node('body_bottom', SnapEngageNode)

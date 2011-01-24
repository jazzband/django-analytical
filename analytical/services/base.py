"""
Base analytical service.
"""
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings



HTML_COMMENT = "<!-- %(message):%(sep)s%(html)s%(sep)s-->"
JS_COMMENT = "*/ %(message):%(sep)s%(html)s%(sep)s*/"
IDENTITY_CONTEXT_KEY = 'analytical_identity'


class AnalyticalService(object):
    """
    Analytics service.
    """

    def render(self, location, context):
        func_name = "render_%s" % location
        func = getattr(self, func_name)
        html = func(context)
        return html

    def render_head_top(self, context):
        return ""

    def render_head_bottom(self, context):
        return ""

    def render_body_top(self, context):
        return ""

    def render_body_bottom(self, context):
        return ""

    def render_event(self, name, properties):
        return ""

    def get_required_setting(self, setting, value_re, invalid_msg):
        try:
            value = getattr(settings, setting)
        except AttributeError:
            raise ImproperlyConfigured("%s setting: not found" % setting)
        value = str(value)
        if not value_re.search(value):
            raise ImproperlyConfigured("%s setting: %s: '%s'"
                    % (setting, invalid_msg, value))
        return value

    def get_identity(self, context):
        try:
            return context[IDENTITY_CONTEXT_KEY]
        except KeyError:
            pass
        if getattr(settings, 'ANALYTICAL_AUTO_IDENTIFY', True):
            try:
                try:
                    user = context['user']
                except KeyError:
                    request = context['request']
                    user = request.user
                if user.is_authenticated():
                    return user.username
            except (KeyError, AttributeError):
                pass
        return None

    def get_events(self, context):
        return context.get('analytical_events', {})

    def get_properties(self, context):
        return context.get('analytical_properties', {})

    def _html_comment(self, html, message=""):
        return self._comment(HTML_COMMENT, html, message)

    def _js_comment(self, html, message=""):
        return self._comment(JS_COMMENT, html, message)

    def _comment(self, format, html, message):
        if not message:
            message = "Disabled"
        if message.find('\n') > -1:
            sep = '\n'
        else:
            sep = ' '
        return format % {'message': message, 'html': html, 'sep': sep}

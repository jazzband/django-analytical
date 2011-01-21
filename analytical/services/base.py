"""
Base analytical service.
"""
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class AnalyticalService(object):
    """
    Analytics service.
    """

    def render(self, location, context):
        func_name = "render_%s" % location
        func = getattr(self, func_name)
        html = func(context)
        if self.is_initialized(context):
            pass
        return html

    def render_head_top(self, context):
        return ""

    def render_head_bottom(self, context):
        return ""

    def render_body_top(self, context):
        return ""

    def render_body_bottom(self, context):
        return ""

    def get_required_setting(self, setting, value_re, invalid_msg):
        try:
            value = getattr(settings, setting)
        except AttributeError:
            raise ImproperlyConfigured("%s setting: not found" % setting)
        value = str(value)
        if not value_re.search(value):
            raise ImproperlyConfigured("%s setting: %s" % (value, invalid_msg))
        return value

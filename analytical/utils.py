"""
Utility function for django-analytical.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


IDENTITY_CONTEXT_KEY = 'analytical_identity'
HTML_COMMENT = "<!-- %(service)s disabled on internal IP address\n%(html)\n-->"


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


def get_identity(context):
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


def is_internal_ip(context):
    try:
        request = context['request']
        remote_ip = request.META.get('HTTP_X_FORWARDED_FOR',
                request.META.get('REMOTE_ADDR', ''))
        return remote_ip in getattr(settings, 'ANALYTICAL_INTERNAL_IPS',
                getattr(settings, 'INTERNAL_IPS', []))
    except KeyError, AttributeError:
        return False


def disable_html(self, html, service):
    return HTML_COMMENT % locals()

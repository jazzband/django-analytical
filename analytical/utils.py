"""
Utility function for django-analytical.
"""

from django.conf import settings


HTML_COMMENT = "<!-- %(service)s disabled on internal IP " \
        "address\n%(html)s\n-->"


def get_required_setting(setting, value_re, invalid_msg):
    try:
        value = getattr(settings, setting)
    except AttributeError:
        raise AnalyticalException("%s setting: not found" % setting)
    value = str(value)
    if not value_re.search(value):
        raise AnalyticalException("%s setting: %s: '%s'"
                % (setting, invalid_msg, value))
    return value


def get_identity(context, prefix=None):
    if prefix is not None:
        try:
            return context['%s_identity' % prefix]
        except KeyError:
            pass
    try:
        return context['analytical_identity']
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


def is_internal_ip(context, prefix=None):
    try:
        request = context['request']
        remote_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if not remote_ip:
            remote_ip = request.META.get('REMOTE_ADDR', '')
        if not remote_ip:
            return False

        internal_ips = ''
        if prefix is not None:
            internal_ips = getattr(settings, '%s_INTERNAL_IPS' % prefix, '')
        if not internal_ips:
            internal_ips = getattr(settings, 'ANALYTICAL_INTERNAL_IPS', '')
        if not internal_ips:
            internal_ips = getattr(settings, 'INTERNAL_IPS', '')

        return remote_ip in internal_ips
    except KeyError, AttributeError:
        return False


def disable_html(html, service):
    return HTML_COMMENT % locals()


class AnalyticalException(Exception):
    """
    Raised when an exception occurs in any django-analytical code that should
    be silenced in templates.
    """
    silent_variable_failure = True

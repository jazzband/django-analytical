"""
Utility function for django-analytical.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

HTML_COMMENT = "<!-- %(service)s disabled on internal IP " \
               "address\n%(html)s\n-->"


def get_required_setting(setting, value_re, invalid_msg):
    """
    Return a constant from ``django.conf.settings``.  The `setting`
    argument is the constant name, the `value_re` argument is a regular
    expression used to validate the setting value and the `invalid_msg`
    argument is used as exception message if the value is not valid.
    """
    try:
        value = getattr(settings, setting)
    except AttributeError:
        raise AnalyticalException("%s setting: not found" % setting)
    if not value:
        raise AnalyticalException("%s setting is not set" % setting)
    value = str(value)
    if not value_re.search(value):
        raise AnalyticalException("%s setting: %s: '%s'"
                                  % (setting, invalid_msg, value))
    return value


def get_user_from_context(context):
    """
    Get the user instance from the template context, if possible.

    If the context does not contain a `request` or `user` attribute,
    `None` is returned.
    """
    try:
        return context['user']
    except KeyError:
        pass
    try:
        request = context['request']
        return request.user
    except (KeyError, AttributeError):
        pass
    return None


def get_user_is_authenticated(user):
    """Check if the user is authenticated.

    This is a compatibility function needed to support both Django 1.x and 2.x;
    Django 2.x turns the function into a proper boolean so function calls will
    fail.
    """
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


def get_identity(context, prefix=None, identity_func=None, user=None):
    """
    Get the identity of a logged in user from a template context.

    The `prefix` argument is used to provide different identities to
    different analytics services.  The `identity_func` argument is a
    function that returns the identity of the user; by default the
    identity is the username.
    """
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
            if user is None:
                user = get_user_from_context(context)
            if get_user_is_authenticated(user):
                if identity_func is not None:
                    return identity_func(user)
                else:
                    return user.get_username()
        except (KeyError, AttributeError):
            pass
    return None


def get_domain(context, prefix):
    """
    Return the domain used for the tracking code.  Each service may be
    configured with its own domain (called `<name>_domain`), or a
    django-analytical-wide domain may be set (using `analytical_domain`.

    If no explicit domain is found in either the context or the
    settings, try to get the domain from the contrib sites framework.
    """
    domain = context.get('%s_domain' % prefix)
    if domain is None:
        domain = context.get('analytical_domain')
    if domain is None:
        domain = getattr(settings, '%s_DOMAIN' % prefix.upper(), None)
    if domain is None:
        domain = getattr(settings, 'ANALYTICAL_DOMAIN', None)
    if domain is None:
        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            from django.contrib.sites.models import Site
            try:
                domain = Site.objects.get_current().domain
            except (ImproperlyConfigured, Site.DoesNotExist):
                pass
    return domain


def is_internal_ip(context, prefix=None):
    """
    Return whether the visitor is coming from an internal IP address,
    based on information from the template context.

    The prefix is used to allow different analytics services to have
    different notions of internal addresses.
    """
    try:
        request = context['request']
        remote_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if not remote_ip:
            remote_ip = request.META.get('REMOTE_ADDR', '')
        if not remote_ip:
            return False

        internal_ips = None
        if prefix is not None:
            internal_ips = getattr(settings, '%s_INTERNAL_IPS' % prefix, None)
        if internal_ips is None:
            internal_ips = getattr(settings, 'ANALYTICAL_INTERNAL_IPS', None)
        if internal_ips is None:
            internal_ips = getattr(settings, 'INTERNAL_IPS', None)

        return remote_ip in (internal_ips or [])
    except (KeyError, AttributeError):
        return False


def disable_html(html, service):
    """
    Disable HTML code by commenting it out.

    The `service` argument is used to display a friendly message.
    """
    return HTML_COMMENT % {'html': html, 'service': service}


class AnalyticalException(Exception):
    """
    Raised when an exception occurs in any django-analytical code that should
    be silenced in templates.
    """
    silent_variable_failure = True

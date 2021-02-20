"""
Matomo template tags and filters.
"""

import re
from collections import namedtuple
from itertools import chain

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    is_internal_ip,
)

# domain name (characters separated by a dot), optional port, optional URI path, no slash
DOMAINPATH_RE = re.compile(r'^(([^./?#@:]+\.)*[^./?#@:]+)+(:[0-9]+)?(/[^/?#@:]+)*$')

# numeric ID
SITEID_RE = re.compile(r'^\d+$')

TRACKING_CODE = """
<script type="text/javascript">
  var _paq = window._paq || [];
  %(variables)s
  %(commands)s
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="//%(url)s/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', %(siteid)s]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="//%(url)s/piwik.php?idsite=%(siteid)s" style="border:0;" alt="" /></p></noscript>
"""  # noqa

VARIABLE_CODE = '_paq.push(["setCustomVariable", %(index)s, "%(name)s", "%(value)s", "%(scope)s"]);'  # noqa
IDENTITY_CODE = '_paq.push(["setUserId", "%(userid)s"]);'
DISABLE_COOKIES_CODE = '_paq.push([\'disableCookies\']);'

DEFAULT_SCOPE = 'page'

MatomoVar = namedtuple('MatomoVar', ('index', 'name', 'value', 'scope'))


register = Library()


@register.tag
def matomo(parser, token):
    """
    Matomo tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Matomo domain (plus optional URI path), and tracked site ID
    in the ``MATOMO_DOMAIN_PATH`` and the ``MATOMO_SITE_ID`` setting.

    Custom variables can be passed in the ``matomo_vars`` context
    variable.  It is an iterable of custom variables as tuples like:
    ``(index, name, value[, scope])`` where scope may be ``'page'``
    (default) or ``'visit'``.  Index should be an integer and the
    other parameters should be strings.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return MatomoNode()


class MatomoNode(Node):
    def __init__(self):
        self.domain_path = \
            get_required_setting('MATOMO_DOMAIN_PATH', DOMAINPATH_RE,
                                 "must be a domain name, optionally followed "
                                 "by an URI path, no trailing slash (e.g. "
                                 "matomo.example.com or my.matomo.server/path)")
        self.site_id = \
            get_required_setting('MATOMO_SITE_ID', SITEID_RE,
                                 "must be a (string containing a) number")

    def render(self, context):
        custom_variables = context.get('matomo_vars', ())

        complete_variables = (var if len(var) >= 4 else var + (DEFAULT_SCOPE,)
                              for var in custom_variables)

        variables_code = (VARIABLE_CODE % MatomoVar(*var)._asdict()
                          for var in complete_variables)

        commands = []
        if getattr(settings, 'MATOMO_DISABLE_COOKIES', False):
            commands.append(DISABLE_COOKIES_CODE)

        userid = get_identity(context, 'matomo')
        if userid is not None:
            variables_code = chain(variables_code, (
                IDENTITY_CODE % {'userid': userid},
            ))

        html = TRACKING_CODE % {
            'url': self.domain_path,
            'siteid': self.site_id,
            'variables': '\n  '.join(variables_code),
            'commands': '\n  '.join(commands)
        }
        if is_internal_ip(context, 'MATOMO'):
            html = disable_html(html, 'Matomo')
        return html


def contribute_to_analytical(add_node):
    MatomoNode()  # ensure properly configured
    add_node('body_bottom', MatomoNode)

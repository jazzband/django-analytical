"""
Piwik template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import is_internal_ip, disable_html, get_required_setting


# domain name (characters separated by a dot), optional URI path, no slash
DOMAINPATH_RE = re.compile(r'^(([^./?#@:]+\.)+[^./?#@:]+)+(/[^/?#@:]+)*$')

# numeric ID
SITEID_RE = re.compile(r'^\d+$')

TRACKING_CODE = """
<script type="text/javascript">
  var _paq = _paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u=(("https:" == document.location.protocol) ? "https" : "http") + "://%(url)s/";
    _paq.push(['setTrackerUrl', u+'piwik.php']);
    _paq.push(['setSiteId', %(siteid)s]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0]; g.type='text/javascript';
    g.defer=true; g.async=true; g.src=u+'piwik.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img src="http://%(url)s/piwik.php?idsite=%(siteid)s" style="border:0;" alt="" /></p></noscript>
"""  # noqa


register = Library()


@register.tag
def piwik(parser, token):
    """
    Piwik tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Piwik domain (plus optional URI path), and tracked site ID
    in the ``PIWIK_DOMAIN_PATH`` and the ``PIWIK_SITE_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return PiwikNode()


class PiwikNode(Node):
    def __init__(self):
        self.domain_path = \
            get_required_setting('PIWIK_DOMAIN_PATH', DOMAINPATH_RE,
                                 "must be a domain name, optionally followed "
                                 "by an URI path, no trailing slash (e.g. "
                                 "piwik.example.com or my.piwik.server/path)")
        self.site_id = \
            get_required_setting('PIWIK_SITE_ID', SITEID_RE,
                                 "must be a (string containing a) number")

    def render(self, context):
        html = TRACKING_CODE % {
            'url': self.domain_path,
            'siteid': self.site_id,
        }
        if is_internal_ip(context, 'PIWIK'):
            html = disable_html(html, 'Piwik')
        return html


def contribute_to_analytical(add_node):
    PiwikNode()  # ensure properly configured
    add_node('body_bottom', PiwikNode)

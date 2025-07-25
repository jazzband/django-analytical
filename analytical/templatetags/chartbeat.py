"""
Chartbeat template tags and filters.
"""

import json
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

USER_ID_RE = re.compile(r'^\d+$')
INIT_CODE = """<script>var _sf_startpt=(new Date()).getTime()</script>"""
SETUP_CODE = """
    <script>
      var _sf_async_config=%(config)s;
      (function(){
        function loadChartbeat() {
          window._sf_endpt=(new Date()).getTime();
          var e = document.createElement('script');
          e.setAttribute('language', 'javascript');
          e.setAttribute('type', 'text/javascript');
          e.setAttribute('src',
             (("https:" == document.location.protocol) ? "https://a248.e.akamai.net/chartbeat.download.akamai.com/102508/" : "http://static.chartbeat.com/") +
             "js/chartbeat.js");
          document.body.appendChild(e);
        }
        var oldonload = window.onload;
        window.onload = (typeof window.onload != 'function') ?
           loadChartbeat : function() { oldonload(); loadChartbeat(); };
      })();
    </script>
"""  # noqa
DOMAIN_CONTEXT_KEY = 'chartbeat_domain'


register = Library()


@register.tag
def chartbeat_top(parser, token):
    """
    Top Chartbeat template tag.

    Render the top JavaScript code for Chartbeat.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ChartbeatTopNode()


class ChartbeatTopNode(Node):
    def render(self, context):
        if is_internal_ip(context):
            return disable_html(INIT_CODE, 'Chartbeat')
        return INIT_CODE


@register.tag
def chartbeat_bottom(parser, token):
    """
    Bottom Chartbeat template tag.

    Render the bottom JavaScript code for Chartbeat.  You must supply
    your Chartbeat User ID (as a string) in the ``CHARTBEAT_USER_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ChartbeatBottomNode()


class ChartbeatBottomNode(Node):
    def __init__(self):
        self.user_id = get_required_setting(
            'CHARTBEAT_USER_ID', USER_ID_RE, 'must be (a string containing) a number'
        )

    def render(self, context):
        config = {'uid': self.user_id}
        domain = _get_domain(context)
        if domain is not None:
            config['domain'] = domain
        html = SETUP_CODE % {'config': json.dumps(config, sort_keys=True)}
        if is_internal_ip(context, 'CHARTBEAT'):
            html = disable_html(html, 'Chartbeat')
        return html


def contribute_to_analytical(add_node):
    ChartbeatBottomNode()  # ensure properly configured
    add_node('head_top', ChartbeatTopNode, 'first')
    add_node('body_bottom', ChartbeatBottomNode, 'last')


def _get_domain(context):
    domain = context.get(DOMAIN_CONTEXT_KEY)

    if domain is not None:
        return domain
    else:
        if 'django.contrib.sites' not in settings.INSTALLED_APPS:
            return
        elif getattr(settings, 'CHARTBEAT_AUTO_DOMAIN', True):
            from django.contrib.sites.models import Site

            try:
                return Site.objects.get_current().domain
            except (ImproperlyConfigured, Site.DoesNotExist):  # pylint: disable=E1101
                return

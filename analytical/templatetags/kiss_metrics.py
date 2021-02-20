"""
KISSmetrics template tags.
"""

import json
import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_identity,
    get_required_setting,
    is_internal_ip,
)

API_KEY_RE = re.compile(r'^[0-9a-f]{40}$')
TRACKING_CODE = """
    <script type="text/javascript">
      var _kmq = _kmq || [];
      %(commands)s
      function _kms(u){
        setTimeout(function(){
          var s = document.createElement('script');
          s.type = 'text/javascript';
          s.async = true;
          s.src = u;
          var f = document.getElementsByTagName('script')[0];
          f.parentNode.insertBefore(s, f);
        }, 1);
      }
      _kms('//i.kissmetrics.com/i.js');
      _kms('//doug1izaerwt3.cloudfront.net/%(api_key)s.1.js');
    </script>
"""
IDENTIFY_CODE = "_kmq.push(['identify', '%s']);"
EVENT_CODE = "_kmq.push(['record', '%(name)s', %(properties)s]);"
PROPERTY_CODE = "_kmq.push(['set', %(properties)s]);"
ALIAS_CODE = "_kmq.push(['alias', '%s', '%s']);"

EVENT_CONTEXT_KEY = 'kiss_metrics_event'
PROPERTY_CONTEXT_KEY = 'kiss_metrics_properties'
ALIAS_CONTEXT_KEY = 'kiss_metrics_alias'

register = Library()


@register.tag
def kiss_metrics(parser, token):
    """
    KISSinsights tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your KISSmetrics API key in the ``KISS_METRICS_API_KEY``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return KissMetricsNode()


class KissMetricsNode(Node):
    def __init__(self):
        self.api_key = get_required_setting(
            'KISS_METRICS_API_KEY', API_KEY_RE,
            "must be a string containing a 40-digit hexadecimal number")

    def render(self, context):
        commands = []
        identity = get_identity(context, 'kiss_metrics')
        if identity is not None:
            commands.append(IDENTIFY_CODE % identity)
        try:
            properties = context[ALIAS_CONTEXT_KEY]
            key, value = properties.popitem()
            commands.append(ALIAS_CODE % (key, value))
        except KeyError:
            pass
        try:
            name, properties = context[EVENT_CONTEXT_KEY]
            commands.append(EVENT_CODE % {
                'name': name,
                'properties': json.dumps(properties, sort_keys=True),
            })
        except KeyError:
            pass
        try:
            properties = context[PROPERTY_CONTEXT_KEY]
            commands.append(PROPERTY_CODE % {
                'properties': json.dumps(properties, sort_keys=True),
            })
        except KeyError:
            pass
        html = TRACKING_CODE % {
            'api_key': self.api_key,
            'commands': " ".join(commands),
        }
        if is_internal_ip(context, 'KISS_METRICS'):
            html = disable_html(html, 'KISSmetrics')
        return html


def contribute_to_analytical(add_node):
    KissMetricsNode()  # ensure properly configured
    add_node('head_top', KissMetricsNode)

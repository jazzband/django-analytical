"""
Google Analytics template tags and filters, using the new gtag.js library.

gtag.js documentation found at: https://developers.google.com/analytics/devguides/collection/gtagjs/
API reference at: https://developers.google.com/gtagjs/reference/api
"""

from __future__ import absolute_import

import re
import json
from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import (
    disable_html,
    get_required_setting,
    is_internal_ip,
)

GA_MEASUREMENT_ID_RE = re.compile(r'[a-zA-Z\d_\-]+')

SETUP_CODE = """
<script async src="https://www.googletagmanager.com/gtag/js?id={property_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  {set_commands}
  gtag('config', '{property_id}', {config_parameters_json});
</script>
"""

CUSTOM_SET_KV_CODE = "gtag('set', '{key}', {value_json});"
CUSTOM_SET_DATA_CODE = "gtag('set', {value_json});"

# You are allowed to config more than one GA_MEASUREMENT_ID on a page.
# This could be used, but for now is not.
CUSTOM_CONFIG_CODE = "gtag('config', '{property_id}', {config_parameters_json});"

register = Library()


@register.tag
def google_gtag_js(parser, token):
    """
    Google Analytics Global Site Tag tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your website property ID (as a string) in the
    ``GOOGLE_GTAG_JS_PROPERTY_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return GoogleGTagJsNode()


class GoogleGTagJsNode(Node):
    def __init__(self):
        self.property_id = get_required_setting(
            'GOOGLE_GTAG_JS_PROPERTY_ID', GA_MEASUREMENT_ID_RE,
            "must be a string like a slug")

    def render(self, context):
        config_parameters = self._get_config_parameters(context)
        config_parameters_json = self._to_json(config_parameters)

        set_commands = self._get_set_commands(context)

        html = SETUP_CODE.format(
            property_id=self.property_id,
            config_parameters_json=config_parameters_json,
            set_commands=" ".join(set_commands),
        )
        if is_internal_ip(context, 'GOOGLE_ANALYTICS'):
            html = disable_html(html, 'Google Analytics')
        return html

    def _get_config_parameters(self, context):
        config_data = getattr(
            settings, 'GOOGLE_GTAG_JS_DEFAULT_CONFIG', {},
        )

        config_data.update(context.get('google_gtag_js_config_data', {}))

        return config_data

    def _to_json(self, data, default="{}"):
        try:
            return json.dumps(data)
        except ValueError:
            return default
        except TypeError:
            return default

    def _get_set_commands(self, context):
        commands = []

        if 'google_gtag_js_set_data' in context:
            try:
                commands.append(CUSTOM_SET_DATA_CODE.format(
                    value_json=json.dumps(context['google_gtag_js_set_data']),
                ))
            except ValueError:
                pass

        values = (
            context.get('google_gtag_js_set%s' % i) for i in range(1, 6)
        )
        params = [(i, v) for i, v in enumerate(values, 1) if v is not None]

        for _, var in params:
            key_name = var[0]
            value = var[1]
            try:
                value_json = json.dumps(value)
            except ValueError:
                value_json = json.dumps(str(value))
            commands.append(CUSTOM_SET_KV_CODE.format(
                key=key_name,
                value_json=value_json,
            ))
        return commands


def contribute_to_analytical(add_node):
    GoogleGTagJsNode()  # ensure properly configured
    add_node('head_top', GoogleGTagJsNode)

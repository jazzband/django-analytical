"""
Yandex.Metrica template tags and filters.
"""

import json
import re

from django.conf import settings
from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

COUNTER_ID_RE = re.compile(r'^\d{8}$')
COUNTER_CODE = """
    <script type="text/javascript">
        (function (d, w, c) {
            (w[c] = w[c] || []).push(function() {
                try {
                    w.yaCounter%(counter_id)s = new Ya.Metrika(%(options)s);
                } catch(e) { }
            });

            var n = d.getElementsByTagName("script")[0],
                s = d.createElement("script"),
                f = function () { n.parentNode.insertBefore(s, n); };
            s.type = "text/javascript";
            s.async = true;
            s.src = "https://mc.yandex.ru/metrika/watch.js";

            if (w.opera == "[object Opera]") {
                d.addEventListener("DOMContentLoaded", f, false);
            } else { f(); }
        })(document, window, "yandex_metrika_callbacks");
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/%(counter_id)s" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
"""  # noqa


register = Library()


@register.tag
def yandex_metrica(parser, token):
    """
    Yandex.Metrica counter template tag.

    Renders Javascript code to track page visits. You must supply
    your website counter ID (as a string) in the
    ``YANDEX_METRICA_COUNTER_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return YandexMetricaNode()


class YandexMetricaNode(Node):
    def __init__(self):
        self.counter_id = get_required_setting(
                'YANDEX_METRICA_COUNTER_ID', COUNTER_ID_RE,
                "must be (a string containing) a number'")

    def render(self, context):
        options = {
            'id': int(self.counter_id),
            'clickmap': True,
            'trackLinks': True,
            'accurateTrackBounce': True
        }
        if getattr(settings, 'YANDEX_METRICA_WEBVISOR', False):
            options['webvisor'] = True
        if getattr(settings, 'YANDEX_METRICA_TRACKHASH', False):
            options['trackHash'] = True
        if getattr(settings, 'YANDEX_METRICA_NOINDEX', False):
            options['ut'] = 'noindex'
        if getattr(settings, 'YANDEX_METRICA_ECOMMERCE', False):
            options['ecommerce'] = 'dataLayer'
        html = COUNTER_CODE % {
            'counter_id': self.counter_id,
            'options': json.dumps(options),
        }
        if is_internal_ip(context, 'YANDEX_METRICA'):
            html = disable_html(html, 'Yandex.Metrica')
        return html


def contribute_to_analytical(add_node):
    YandexMetricaNode()  # ensure properly configured
    add_node('head_bottom', YandexMetricaNode)

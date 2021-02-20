"""
Rating@Mail.ru template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

COUNTER_ID_RE = re.compile(r'^\d{7}$')
COUNTER_CODE = """
    <script type="text/javascript">
    var _tmr = window._tmr || (window._tmr = []);
    _tmr.push({id: "%(counter_id)s", type: "pageView", start: (new Date()).getTime()});
    (function (d, w, id) {
      if (d.getElementById(id)) return;
      var ts = d.createElement("script"); ts.type = "text/javascript"; ts.async = true; ts.id = id;
      ts.src = (d.location.protocol == "https:" ? "https:" : "http:") + "//top-fwz1.mail.ru/js/code.js";
      var f = function () {var s = d.getElementsByTagName("script")[0]; s.parentNode.insertBefore(ts, s);};
      if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); }
    })(document, window, "topmailru-code");
    </script>
    <noscript><div style="position:absolute;left:-10000px;">
    <img src="//top-fwz1.mail.ru/counter?id=%(counter_id)s;js=na" style="border:0;" height="1" width="1" alt="Rating@Mail.ru" />
    </div></noscript>
"""  # noqa


register = Library()


@register.tag
def rating_mailru(parser, token):
    """
    Rating@Mail.ru counter template tag.

    Renders Javascript code to track page visits. You must supply
    your website counter ID (as a string) in the
    ``RATING_MAILRU_COUNTER_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return RatingMailruNode()


class RatingMailruNode(Node):
    def __init__(self):
        self.counter_id = get_required_setting(
            'RATING_MAILRU_COUNTER_ID', COUNTER_ID_RE,
            "must be (a string containing) a number'")

    def render(self, context):
        html = COUNTER_CODE % {
            'counter_id': self.counter_id,
        }
        if is_internal_ip(context, 'RATING_MAILRU_METRICA'):
            html = disable_html(html, 'Rating@Mail.ru')
        return html


def contribute_to_analytical(add_node):
    RatingMailruNode()  # ensure properly configured
    add_node('head_bottom', RatingMailruNode)

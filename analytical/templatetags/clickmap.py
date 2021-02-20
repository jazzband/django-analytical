"""
Clickmap template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

CLICKMAP_TRACKER_ID_RE = re.compile(r'^\w+$')
TRACKING_CODE = """
    <script type="text/javascript">
    var clickmapConfig = {tracker: '%(tracker_id)s', version:'2'};
    window.clickmapAsyncInit = function(){ __clickmap.init(clickmapConfig); };
    (function() { var _cmf = document.createElement('script'); _cmf.async = true;
    _cmf.src = document.location.protocol + '//www.clickmap.ch/tracker.js?t=';
    _cmf.src += clickmapConfig.tracker; _cmf.id += 'clickmap_tracker';
    _cmf.src += '&v='+clickmapConfig.version+'&now='+(new Date().getTime());
    if (document.getElementById('clickmap_tracker')==null) {
    document.getElementsByTagName('head')[0].appendChild(_cmf); }}());
    </script>
"""

register = Library()


@register.tag
def clickmap(parser, token):
    """
    Clickmap tracker template tag.

    Renders Javascript code to track page visits.  You must supply
    your clickmap tracker ID (as a string) in the ``CLICKMAP_TRACKER_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ClickmapNode()


class ClickmapNode(Node):
    def __init__(self):
        self.tracker_id = get_required_setting('CLICKMAP_TRACKER_ID',
                                               CLICKMAP_TRACKER_ID_RE,
                                               "must be an alphanumeric string")

    def render(self, context):
        html = TRACKING_CODE % {'tracker_id': self.tracker_id}
        if is_internal_ip(context, 'CLICKMAP'):
            html = disable_html(html, 'Clickmap')
        return html


def contribute_to_analytical(add_node):
    ClickmapNode()  # ensure properly configured
    add_node('body_bottom', ClickmapNode)

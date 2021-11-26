"""
Heap template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

HEAP_TRACKER_ID_RE = re.compile(r'^\d+$')
TRACKING_CODE = """
<script type="text/javascript">
  window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])}; 
  heap.load("%(tracker_id)s");
</script>

""" # noqa

register = Library()


def _validate_no_args(token):
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])


@register.tag
def heap(parser, token):
    """
    Heap tracker template tag.

    Renders Javascript code to track page visits.  You must supply
    your heap tracker ID (as a string) in the ``HEAP_TRACKER_ID``
    setting.
    """
    _validate_no_args(token)
    return HeapNode()


class HeapNode(Node):
    def __init__(self):
        self.tracker_id = get_required_setting('HEAP_TRACKER_ID',
                                               HEAP_TRACKER_ID_RE,
                                               "must be an numeric string")

    def render(self, context):
        html = TRACKING_CODE % {'tracker_id': self.tracker_id}
        if is_internal_ip(context, 'HEAP'):
            html = disable_html(html, 'Heap')
        return html


def contribute_to_analytical(add_node):
    HeapNode()  # ensure properly configured
    add_node('head_bottom', HeapNode)

"""
Facebook Pixel template tags and filters.
"""

import re

from django.template import Library, Node, TemplateSyntaxError

from analytical.utils import disable_html, get_required_setting, is_internal_ip

FACEBOOK_PIXEL_HEAD_CODE = """\
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '%(FACEBOOK_PIXEL_ID)s');
  fbq('track', 'PageView');
</script>
"""

FACEBOOK_PIXEL_BODY_CODE = """\
<noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=%(FACEBOOK_PIXEL_ID)s&ev=PageView&noscript=1"
/></noscript>
"""

register = Library()


def _validate_no_args(token):
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])


@register.tag
def facebook_pixel_head(parser, token):
    """
    Facebook Pixel head template tag.
    """
    _validate_no_args(token)
    return FacebookPixelHeadNode()


@register.tag
def facebook_pixel_body(parser, token):
    """
    Facebook Pixel body template tag.
    """
    _validate_no_args(token)
    return FacebookPixelBodyNode()


class _FacebookPixelNode(Node):
    """
    Base class: override and provide code_template.
    """
    def __init__(self):
        self.pixel_id = get_required_setting(
            'FACEBOOK_PIXEL_ID',
            re.compile(r'^\d+$'),
            "must be (a string containing) a number",
        )

    def render(self, context):
        html = self.code_template % {'FACEBOOK_PIXEL_ID': self.pixel_id}
        if is_internal_ip(context, 'FACEBOOK_PIXEL'):
            return disable_html(html, 'Facebook Pixel')
        else:
            return html

    @property
    def code_template(self):
        raise NotImplementedError  # pragma: no cover


class FacebookPixelHeadNode(_FacebookPixelNode):
    code_template = FACEBOOK_PIXEL_HEAD_CODE


class FacebookPixelBodyNode(_FacebookPixelNode):
    code_template = FACEBOOK_PIXEL_BODY_CODE


def contribute_to_analytical(add_node):
    # ensure properly configured
    FacebookPixelHeadNode()
    FacebookPixelBodyNode()
    add_node('head_bottom', FacebookPixelHeadNode)
    add_node('body_bottom', FacebookPixelBodyNode)

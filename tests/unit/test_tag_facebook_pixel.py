"""
Tests for the Facebook Pixel template tags.
"""
from django.http import HttpRequest
from django.template import Context, Template, TemplateSyntaxError
from django.test import override_settings

from analytical.templatetags.analytical import _load_template_nodes
from analytical.templatetags.facebook_pixel import FacebookPixelHeadNode, FacebookPixelBodyNode
from utils import TagTestCase
from analytical.utils import AnalyticalException

import pytest

expected_head_html = """\
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '1234567890');
  fbq('track', 'PageView');
</script>
"""


expected_body_html = """\
<noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=1234567890&ev=PageView&noscript=1"
/></noscript>
"""


@override_settings(FACEBOOK_PIXEL_ID='1234567890')
class FacebookPixelTagTestCase(TagTestCase):

    maxDiff = None

    def test_head_tag(self):
        html = self.render_tag('facebook_pixel', 'facebook_pixel_head')
        assert expected_head_html == html

    def test_head_node(self):
        html = FacebookPixelHeadNode().render(Context({}))
        assert expected_head_html == html

    def test_body_tag(self):
        html = self.render_tag('facebook_pixel', 'facebook_pixel_body')
        assert expected_body_html == html

    def test_body_node(self):
        html = FacebookPixelBodyNode().render(Context({}))
        assert expected_body_html == html

    def test_tags_take_no_args(self):
        template = '{%% load facebook_pixel %%}{%% facebook_pixel_%s "arg" %%}'
        with pytest.raises(TemplateSyntaxError, match="'facebook_pixel_head' takes no arguments"):
            Template(template % "head").render(Context({}))

        with pytest.raises(TemplateSyntaxError, match="'facebook_pixel_body' takes no arguments"):
            Template(template % "body").render(Context({}))

    @override_settings(FACEBOOK_PIXEL_ID=None)
    def test_no_id(self):
        expected_pattern = 'FACEBOOK_PIXEL_ID setting is not set'
        with pytest.raises(AnalyticalException, match=expected_pattern):
            FacebookPixelHeadNode()
        with pytest.raises(AnalyticalException, match=expected_pattern):
            FacebookPixelBodyNode()

    @override_settings(FACEBOOK_PIXEL_ID='invalid')
    def test_invalid_id(self):
        expected_pattern = (
            r"FACEBOOK_PIXEL_ID setting: must be \(a string containing\) a number: 'invalid'$"
        )
        with pytest.raises(AnalyticalException, match=expected_pattern):
            FacebookPixelHeadNode()
        with pytest.raises(AnalyticalException, match=expected_pattern):
            FacebookPixelBodyNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': request})

        def _disabled(html):
            return '\n'.join([
                '<!-- Facebook Pixel disabled on internal IP address',
                html,
                '-->',
            ])

        head_html = FacebookPixelHeadNode().render(context)
        assert _disabled(expected_head_html) == head_html

        body_html = FacebookPixelBodyNode().render(context)
        assert _disabled(expected_body_html) == body_html

    def test_contribute_to_analytical(self):
        """
        `facebook_pixel.contribute_to_analytical` registers the head and body nodes.
        """
        template_nodes = _load_template_nodes()
        assert template_nodes == {
            'head_top': [],
            'head_bottom': [FacebookPixelHeadNode],
            'body_top': [],
            'body_bottom': [FacebookPixelBodyNode],
        }

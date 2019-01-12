"""
Tests for the Hotjar template tags.
"""
from django.http import HttpRequest
from django.template import Context, Template, TemplateSyntaxError
from django.test import override_settings

from analytical.templatetags.analytical import _load_template_nodes
from analytical.templatetags.hotjar import HotjarNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


expected_html = """\
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:123456789,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""


@override_settings(HOTJAR_SITE_ID='123456789')
class HotjarTagTestCase(TagTestCase):

    maxDiff = None

    def test_tag(self):
        html = self.render_tag('hotjar', 'hotjar')
        self.assertEqual(expected_html, html)

    def test_node(self):
        html = HotjarNode().render(Context({}))
        self.assertEqual(expected_html, html)

    def test_tags_take_no_args(self):
        self.assertRaisesRegexp(
            TemplateSyntaxError,
            r"^'hotjar' takes no arguments$",
            lambda: (Template('{% load hotjar %}{% hotjar "arg" %}')
                     .render(Context({}))),
        )

    @override_settings(HOTJAR_SITE_ID=None)
    def test_no_id(self):
        expected_pattern = r'^HOTJAR_SITE_ID setting is not set$'
        self.assertRaisesRegexp(AnalyticalException, expected_pattern, HotjarNode)

    @override_settings(HOTJAR_SITE_ID='invalid')
    def test_invalid_id(self):
        expected_pattern = (
            r"^HOTJAR_SITE_ID setting: must be \(a string containing\) a number: 'invalid'$")
        self.assertRaisesRegexp(AnalyticalException, expected_pattern, HotjarNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': request})

        actual_html = HotjarNode().render(context)
        disabled_html = '\n'.join([
                '<!-- Hotjar disabled on internal IP address',
                expected_html,
                '-->',
            ])
        self.assertEqual(disabled_html, actual_html)

    def test_contribute_to_analytical(self):
        """
        `hotjar.contribute_to_analytical` registers the head and body nodes.
        """
        template_nodes = _load_template_nodes()
        self.assertEqual({
            'head_top': [],
            'head_bottom': [HotjarNode],
            'body_top': [],
            'body_bottom': [],
        }, template_nodes)

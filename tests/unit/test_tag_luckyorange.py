"""
Tests for the Lucky Orange template tags.
"""
from django.http import HttpRequest
from django.template import Context, Template, TemplateSyntaxError
from django.test import override_settings

from analytical.templatetags.analytical import _load_template_nodes
from analytical.templatetags.luckyorange import LuckyOrangeNode
from utils import TagTestCase
from analytical.utils import AnalyticalException


expected_html = """\
<script type='text/javascript'>
window.__lo_site_id = 123456;
(function() {
    var wa = document.createElement('script'); wa.type = 'text/javascript'; wa.async = true;
    wa.src = 'https://d10lpsik1i8c69.cloudfront.net/w.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(wa, s);
})();
</script>
"""


@override_settings(LUCKYORANGE_SITE_ID='123456')
class LuckyOrangeTagTestCase(TagTestCase):

    maxDiff = None

    def test_tag(self):
        html = self.render_tag('luckyorange', 'luckyorange')
        self.assertEqual(expected_html, html)

    def test_node(self):
        html = LuckyOrangeNode().render(Context({}))
        self.assertEqual(expected_html, html)

    def test_tags_take_no_args(self):
        self.assertRaisesRegex(
            TemplateSyntaxError,
            r"^'luckyorange' takes no arguments$",
            lambda: (Template('{% load luckyorange %}{% luckyorange "arg" %}')
                     .render(Context({}))),
        )

    @override_settings(LUCKYORANGE_SITE_ID=None)
    def test_no_id(self):
        expected_pattern = r'^LUCKYORANGE_SITE_ID setting is not set$'
        self.assertRaisesRegex(AnalyticalException, expected_pattern, LuckyOrangeNode)

    @override_settings(LUCKYORANGE_SITE_ID='invalid')
    def test_invalid_id(self):
        expected_pattern = (
            r"^LUCKYORANGE_SITE_ID setting: must be \(a string containing\) a number: 'invalid'$")
        self.assertRaisesRegex(AnalyticalException, expected_pattern, LuckyOrangeNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': request})

        actual_html = LuckyOrangeNode().render(context)
        disabled_html = '\n'.join([
                '<!-- Lucky Orange disabled on internal IP address',
                expected_html,
                '-->',
            ])
        self.assertEqual(disabled_html, actual_html)

    def test_contribute_to_analytical(self):
        """
        `luckyorange.contribute_to_analytical` registers the head and body nodes.
        """
        template_nodes = _load_template_nodes()
        self.assertEqual({
            'head_top': [],
            'head_bottom': [LuckyOrangeNode],
            'body_top': [],
            'body_bottom': [],
        }, template_nodes)

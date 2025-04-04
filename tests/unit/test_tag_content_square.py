"""
Tests for the Contentsquare template tags.
"""
import pytest
from django.http import HttpRequest
from django.template import Context, Template, TemplateSyntaxError
from django.test import override_settings
from utils import TagTestCase

from analytical.templatetags.analytical import _load_template_nodes
from analytical.templatetags.contentsquare import ContentsquareNode
from analytical.utils import AnalyticalException

expected_html = """\
<script>
    (function (c, s, q, u, a, r, e) {
        c.hj = c.hj || function(){ (c.hj.q = c.hj.q || []).push(arguments) };
        c._hjSettings = { hjid: 123456789 };
        r = s.getElementsByTagName('head')[0];
        e = s.createElement('script');
        e.async = true;
        e.src = q + c._hjSettings.hjid + u;
        r.appendChild(e);
    })(window, document, 'https://static.hj.contentsquare.net/c/csq-', '.js', 123456789);
</script>
"""

@override_settings(CONTENTSQUARE_SITE_ID='123456789')
class ContentsquareTagTestCase(TagTestCase):

    maxDiff = None

    def test_tag(self):
        html = self.render_tag('contentsquare', 'contentsquare')
        assert expected_html == html

    def test_node(self):
        html = ContentsquareNode().render(Context({}))
        assert expected_html == html

    def test_tags_take_no_args(self):
        with pytest.raises(TemplateSyntaxError, match="'contentsquare' takes no arguments"):
            Template('{% load contentsquare %}{% contentsquare "arg" %}').render(Context({}))

    @override_settings(CONTENTSQUARE_SITE_ID=None)
    def test_no_id(self):
        with pytest.raises(AnalyticalException, match="CONTENTSQUARE_SITE_ID setting is not set"):
            ContentsquareNode()

    @override_settings(CONTENTSQUARE_SITE_ID='invalid')
    def test_invalid_id(self):
        expected_pattern = (
            r"^CONTENTSQUARE_SITE_ID setting: must be \(a string containing\) a number: 'invalid'$")
        with pytest.raises(AnalyticalException, match=expected_pattern):
            ContentsquareNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': request})

        actual_html = ContentsquareNode().render(context)
        disabled_html = '\n'.join([
            '<!-- Contentsquare disabled on internal IP address',
            expected_html,
            '-->',
        ])
        assert disabled_html == actual_html

    def test_contribute_to_analytical(self):
        """
        `contentsquare.contribute_to_analytical` registers the head and body nodes.
        """
        template_nodes = _load_template_nodes()
        assert template_nodes == {
            'head_top': [],
            'head_bottom': [ContentsquareNode],
            'body_top': [],
            'body_bottom': [],
        }

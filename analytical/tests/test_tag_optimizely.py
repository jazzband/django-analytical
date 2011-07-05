"""
Tests for the Optimizely template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.optimizely import OptimizelyNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(OPTIMIZELY_ACCOUNT_NUMBER='1234567')
class OptimizelyTagTestCase(TagTestCase):
    """
    Tests for the ``optimizely`` template tag.
    """

    def test_tag(self):
        self.assertEqual(
                '<script src="//cdn.optimizely.com/js/1234567.js"></script>',
                self.render_tag('optimizely', 'optimizely'))

    def test_node(self):
        self.assertEqual(
                '<script src="//cdn.optimizely.com/js/1234567.js"></script>',
                OptimizelyNode().render(Context()))

    @override_settings(OPTIMIZELY_ACCOUNT_NUMBER=SETTING_DELETED)
    def test_no_account_number(self):
        self.assertRaises(AnalyticalException, OptimizelyNode)

    @override_settings(OPTIMIZELY_ACCOUNT_NUMBER='123abc')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, OptimizelyNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = OptimizelyNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Optimizely disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

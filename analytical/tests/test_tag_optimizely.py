"""
Tests for the Optimizely template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.optimizely import OptimizelyNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class OptimizelyTagTestCase(TagTestCase):
    """
    Tests for the ``optimizely`` template tag.
    """

    def setUp(self):
        super(OptimizelyTagTestCase, self).setUp()
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='1234567')

    def test_tag(self):
        self.assertEqual(
                '<script src="//cdn.optimizely.com/js/1234567.js"></script>',
                self.render_tag('optimizely', 'optimizely'))

    def test_node(self):
        self.assertEqual(
                '<script src="//cdn.optimizely.com/js/1234567.js"></script>',
                OptimizelyNode().render(Context()))

    def test_no_account_number(self):
        self.settings_manager.delete('OPTIMIZELY_ACCOUNT_NUMBER')
        self.assertRaises(AnalyticalException, OptimizelyNode)

    def test_wrong_account_number(self):
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='123456')
        self.assertRaises(AnalyticalException, OptimizelyNode)
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='12345678')
        self.assertRaises(AnalyticalException, OptimizelyNode)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = OptimizelyNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Optimizely disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

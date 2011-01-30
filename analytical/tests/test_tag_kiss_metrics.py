"""
Tests for the KISSmetrics tags and filters.
"""

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.kiss_metrics import KissMetricsNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class KissMetricsTagTestCase(TagTestCase):
    """
    Tests for the ``kiss_metrics`` template tag.
    """

    def setUp(self):
        super(KissMetricsTagTestCase, self).setUp()
        self.settings_manager.set(KISS_METRICS_API_KEY='0123456789abcdef012345'
                '6789abcdef01234567')

    def test_tag(self):
        r = self.render_tag('kiss_metrics', 'kiss_metrics')
        self.assertTrue("//doug1izaerwt3.cloudfront.net/0123456789abcdef012345"
                "6789abcdef01234567.1.js" in r, r)

    def test_node(self):
        r = KissMetricsNode().render(Context())
        self.assertTrue("//doug1izaerwt3.cloudfront.net/0123456789abcdef012345"
                "6789abcdef01234567.1.js" in r, r)

    def test_no_api_key(self):
        self.settings_manager.delete('KISS_METRICS_API_KEY')
        self.assertRaises(AnalyticalException, KissMetricsNode)

    def test_wrong_api_key(self):
        self.settings_manager.set(KISS_METRICS_API_KEY='0123456789abcdef012345'
                '6789abcdef0123456')
        self.assertRaises(AnalyticalException, KissMetricsNode)
        self.settings_manager.set(KISS_METRICS_API_KEY='0123456789abcdef012345'
                '6789abcdef012345678')
        self.assertRaises(AnalyticalException, KissMetricsNode)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = KissMetricsNode().render(Context({'user': User(username='test')}))
        self.assertTrue("_kmq.push(['identify', 'test']);" in r, r)

    def test_event(self):
        r = KissMetricsNode().render(Context({'kiss_metrics_event':
                ('test_event', {'prop1': 'val1', 'prop2': 'val2'})}))
        self.assertTrue("_kmq.push(['record', 'test_event', "
                '{"prop1": "val1", "prop2": "val2"}]);' in r, r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = KissMetricsNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- KISSmetrics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

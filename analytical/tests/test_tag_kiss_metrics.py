"""
Tests for the KISSmetrics tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.kiss_metrics import KissMetricsNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(KISS_METRICS_API_KEY='0123456789abcdef0123456789abcdef'
        '01234567')
class KissMetricsTagTestCase(TagTestCase):
    """
    Tests for the ``kiss_metrics`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('kiss_metrics', 'kiss_metrics')
        self.assertTrue("//doug1izaerwt3.cloudfront.net/0123456789abcdef012345"
                "6789abcdef01234567.1.js" in r, r)

    def test_node(self):
        r = KissMetricsNode().render(Context())
        self.assertTrue("//doug1izaerwt3.cloudfront.net/0123456789abcdef012345"
                "6789abcdef01234567.1.js" in r, r)

    @override_settings(KISS_METRICS_API_KEY=SETTING_DELETED)
    def test_no_api_key(self):
        self.assertRaises(AnalyticalException, KissMetricsNode)

    @override_settings(KISS_METRICS_API_KEY='0123456789abcdef0123456789abcdef'
            '0123456')
    def test_api_key_too_short(self):
        self.assertRaises(AnalyticalException, KissMetricsNode)

    @override_settings(KISS_METRICS_API_KEY='0123456789abcdef0123456789abcdef'
            '012345678')
    def test_api_key_too_long(self):
        self.assertRaises(AnalyticalException, KissMetricsNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = KissMetricsNode().render(Context({'user': User(username='test')}))
        self.assertTrue("_kmq.push(['identify', 'test']);" in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = KissMetricsNode().render(Context({'user': AnonymousUser()}))
        self.assertFalse("_kmq.push(['identify', " in r, r)

    def test_event(self):
        r = KissMetricsNode().render(Context({'kiss_metrics_event':
                ('test_event', {'prop1': 'val1', 'prop2': 'val2'})}))
        self.assertTrue("_kmq.push(['record', 'test_event', "
                '{"prop1": "val1", "prop2": "val2"}]);' in r, r)

    def test_property(self):
        r = KissMetricsNode().render(Context({'kiss_metrics_properties':
                {'prop1': 'val1', 'prop2': 'val2'}}))
        self.assertTrue("_kmq.push(['set', "
                '{"prop1": "val1", "prop2": "val2"}]);' in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = KissMetricsNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- KISSmetrics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

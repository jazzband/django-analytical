"""
Tests for the KISSmetrics tags and filters.
"""

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.kiss_metrics import KissMetricsNode
from analytical.utils import AnalyticalException


@override_settings(KISS_METRICS_API_KEY='0123456789abcdef0123456789abcdef01234567')
class KissMetricsTagTestCase(TagTestCase):
    """
    Tests for the ``kiss_metrics`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('kiss_metrics', 'kiss_metrics')
        assert "//doug1izaerwt3.cloudfront.net/0123456789abcdef0123456789abcdef01234567.1.js" in r

    def test_node(self):
        r = KissMetricsNode().render(Context())
        assert "//doug1izaerwt3.cloudfront.net/0123456789abcdef0123456789abcdef01234567.1.js" in r

    @override_settings(KISS_METRICS_API_KEY=None)
    def test_no_api_key(self):
        with pytest.raises(AnalyticalException):
            KissMetricsNode()

    @override_settings(KISS_METRICS_API_KEY='0123456789abcdef0123456789abcdef0123456')
    def test_api_key_too_short(self):
        with pytest.raises(AnalyticalException):
            KissMetricsNode()

    @override_settings(KISS_METRICS_API_KEY='0123456789abcdef0123456789abcdef012345678')
    def test_api_key_too_long(self):
        with pytest.raises(AnalyticalException):
            KissMetricsNode()

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = KissMetricsNode().render(Context({'user': User(username='test')}))
        assert "_kmq.push(['identify', 'test']);" in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = KissMetricsNode().render(Context({'user': AnonymousUser()}))
        assert "_kmq.push(['identify', " not in r

    def test_event(self):
        r = KissMetricsNode().render(Context({
            'kiss_metrics_event': ('test_event', {'prop1': 'val1', 'prop2': 'val2'}),
        }))
        assert "_kmq.push(['record', 'test_event', "
        '{"prop1": "val1", "prop2": "val2"}]);' in r

    def test_property(self):
        r = KissMetricsNode().render(Context({
            'kiss_metrics_properties': {'prop1': 'val1', 'prop2': 'val2'},
        }))
        assert '_kmq.push([\'set\', {"prop1": "val1", "prop2": "val2"}]);' in r

    def test_alias(self):
        r = KissMetricsNode().render(Context({
            'kiss_metrics_alias': {'test': 'test_alias'},
        }))
        assert "_kmq.push(['alias', 'test', 'test_alias']);" in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = KissMetricsNode().render(context)
        assert r.startswith('<!-- KISSmetrics disabled on internal IP address')
        assert r.endswith('-->')

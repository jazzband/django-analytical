"""
Tests for the Spring Metrics template tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.spring_metrics import SpringMetricsNode
from utils import TagTestCase
from analytical.utils import AnalyticalException

import pytest


@override_settings(SPRING_METRICS_TRACKING_ID='12345678')
class SpringMetricsTagTestCase(TagTestCase):
    """
    Tests for the ``spring_metrics`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('spring_metrics', 'spring_metrics')
        assert "_springMetq.push(['id', '12345678']);" in r

    def test_node(self):
        r = SpringMetricsNode().render(Context({}))
        assert "_springMetq.push(['id', '12345678']);" in r

    @override_settings(SPRING_METRICS_TRACKING_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            SpringMetricsNode()

    @override_settings(SPRING_METRICS_TRACKING_ID='123xyz')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            SpringMetricsNode()

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = SpringMetricsNode().render(Context({
            'user': User(email='test@test.com'),
        }))
        assert "_springMetq.push(['setdata', {'email': 'test@test.com'}]);" in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = SpringMetricsNode().render(Context({'user': AnonymousUser()}))
        assert "_springMetq.push(['setdata', {'email':" not in r

    def test_custom(self):
        r = SpringMetricsNode().render(Context({
            'spring_metrics_var1': 'val1',
            'spring_metrics_var2': 'val2',
        }))
        assert "_springMetq.push(['setdata', {'var1': 'val1'}]);" in r
        assert "_springMetq.push(['setdata', {'var2': 'val2'}]);" in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = SpringMetricsNode().render(context)
        assert r.startswith('<!-- Spring Metrics disabled on internal IP address')
        assert r.endswith('-->')

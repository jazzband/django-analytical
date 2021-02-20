"""
Tests for the Mixpanel tags and filters.
"""

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.mixpanel import MixpanelNode
from analytical.utils import AnalyticalException


@override_settings(MIXPANEL_API_TOKEN='0123456789abcdef0123456789abcdef')
class MixpanelTagTestCase(TagTestCase):
    """
    Tests for the ``mixpanel`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('mixpanel', 'mixpanel')
        assert "mixpanel.init('0123456789abcdef0123456789abcdef');" in r

    def test_node(self):
        r = MixpanelNode().render(Context())
        assert "mixpanel.init('0123456789abcdef0123456789abcdef');" in r

    @override_settings(MIXPANEL_API_TOKEN=None)
    def test_no_token(self):
        with pytest.raises(AnalyticalException):
            MixpanelNode()

    @override_settings(MIXPANEL_API_TOKEN='0123456789abcdef0123456789abcdef0')
    def test_token_too_long(self):
        with pytest.raises(AnalyticalException):
            MixpanelNode()

    @override_settings(MIXPANEL_API_TOKEN='0123456789abcdef0123456789abcde')
    def test_token_too_short(self):
        with pytest.raises(AnalyticalException):
            MixpanelNode()

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = MixpanelNode().render(Context({'user': User(username='test')}))
        assert "mixpanel.identify('test');" in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = MixpanelNode().render(Context({'user': AnonymousUser()}))
        assert "mixpanel.register_once({distinct_id:" not in r

    def test_event(self):
        r = MixpanelNode().render(Context({
            'mixpanel_event': ('test_event', {'prop1': 'val1', 'prop2': 'val2'}),
        }))
        assert "mixpanel.track('test_event', "
        '{"prop1": "val1", "prop2": "val2"});' in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = MixpanelNode().render(context)
        assert r.startswith('<!-- Mixpanel disabled on internal IP address')
        assert r.endswith('-->')

"""
Tests for the Mixpanel tags and filters.
"""

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.mixpanel import MixpanelNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(MIXPANEL_API_TOKEN='0123456789abcdef0123456789abcdef')
class MixpanelTagTestCase(TagTestCase):
    """
    Tests for the ``mixpanel`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('mixpanel', 'mixpanel')
        self.assertTrue(
                "mpq.push(['init', '0123456789abcdef0123456789abcdef']);" in r,
                r)

    def test_node(self):
        r = MixpanelNode().render(Context())
        self.assertTrue(
                "mpq.push(['init', '0123456789abcdef0123456789abcdef']);" in r,
                r)

    @override_settings(MIXPANEL_API_TOKEN=SETTING_DELETED)
    def test_no_token(self):
        self.assertRaises(AnalyticalException, MixpanelNode)

    @override_settings(MIXPANEL_API_TOKEN='0123456789abcdef0123456789abcdef0')
    def test_token_too_long(self):
        self.assertRaises(AnalyticalException, MixpanelNode)

    @override_settings(MIXPANEL_API_TOKEN='0123456789abcdef0123456789abcde')
    def test_token_too_short(self):
        self.assertRaises(AnalyticalException, MixpanelNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = MixpanelNode().render(Context({'user': User(username='test')}))
        self.assertTrue("mpq.push(['identify', 'test']);" in r, r)

    def test_event(self):
        r = MixpanelNode().render(Context({'mixpanel_event':
                ('test_event', {'prop1': 'val1', 'prop2': 'val2'})}))
        self.assertTrue("mpq.push(['track', 'test_event', "
                '{"prop1": "val1", "prop2": "val2"}]);' in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = MixpanelNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Mixpanel disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

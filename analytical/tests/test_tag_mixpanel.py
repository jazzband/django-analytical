"""
Tests for the Mixpanel tags and filters.
"""

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.mixpanel import MixpanelNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class MixpanelTagTestCase(TagTestCase):
    """
    Tests for the ``mixpanel`` template tag.
    """

    def setUp(self):
        super(MixpanelTagTestCase, self).setUp()
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='1234567')
        self.settings_manager.set(
                MIXPANEL_TOKEN='0123456789abcdef0123456789abcdef')

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

    def test_no_token(self):
        self.settings_manager.delete('MIXPANEL_TOKEN')
        self.assertRaises(AnalyticalException, MixpanelNode)

    def test_wrong_token(self):
        self.settings_manager.set(
                MIXPANEL_TOKEN='0123456789abcdef0123456789abcde')
        self.assertRaises(AnalyticalException, MixpanelNode)
        self.settings_manager.set(
                MIXPANEL_TOKEN='0123456789abcdef0123456789abcdef0')
        self.assertRaises(AnalyticalException, MixpanelNode)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = MixpanelNode().render(Context({'user': User(username='test')}))
        self.assertTrue("mpq.push(['identify', 'test']);" in r, r)

    def test_event(self):
        r = MixpanelNode().render(Context({'mixpanel_event':
                ('test_event', {'prop1': 'val1', 'prop2': 'val2'})}))
        self.assertTrue("mpq.push(['track', 'test_event', "
                '{"prop1": "val1", "prop2": "val2"}]);' in r, r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = MixpanelNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Mixpanel disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

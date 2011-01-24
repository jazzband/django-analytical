"""
Tests for the Mixpanel service.
"""

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.mixpanel import MixpanelService
from analytical.tests.utils import TestSettingsManager


class MixpanelTestCase(TestCase):
    """
    Tests for the Mixpanel service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(
                MIXPANEL_TOKEN='0123456789abcdef0123456789abcdef')
        self.service = MixpanelService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_top({}), "")
        self.assertEqual(self.service.render_body_top({}), "")
        self.assertEqual(self.service.render_body_bottom({}), "")

    def test_no_token(self):
        self.settings_manager.delete('MIXPANEL_TOKEN')
        self.assertRaises(ImproperlyConfigured, MixpanelService)

    def test_wrong_token(self):
        self.settings_manager.set(
                MIXPANEL_TOKEN='0123456789abcdef0123456789abcde')
        self.assertRaises(ImproperlyConfigured, MixpanelService)
        self.settings_manager.set(
                MIXPANEL_TOKEN='0123456789abcdef0123456789abcdef0')
        self.assertRaises(ImproperlyConfigured, MixpanelService)

    def test_rendering(self):
        r = self.service.render_head_bottom({})
        self.assertTrue(
                "mpq.push(['init', '0123456789abcdef0123456789abcdef']);" in r,
                r)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = self.service.render_head_bottom({'user': User(username='test')})
        self.assertTrue("mpq.push(['identify', 'test']);" in r, r)

    def test_event(self):
        r = self.service.render_event('test_event', {'prop1': 'val1',
                'prop2': 'val2'})
        self.assertEqual(r, "mpq.push(['track', 'test_event', "
                '{"prop1": "val1", "prop2": "val2"}]);')

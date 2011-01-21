"""
Tests for the Mixpanel service.
"""

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
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_top({}), "")

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
        r = self.service.render_body_bottom({})
        self.assertTrue("MixpanelLib('0123456789abcdef0123456789abcdef')" in r,
                r)

"""
Tests for the Crazy Egg service.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.crazy_egg import CrazyEggService
from analytical.tests.utils import TestSettingsManager


class CrazyEggTestCase(TestCase):
    """
    Tests for the Crazy Egg service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(CRAZY_EGG_ACCOUNT_NUMBER='12345678')
        self.service = CrazyEggService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_top({}), "")
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_top({}), "")

    def test_no_account_number(self):
        self.settings_manager.delete('CRAZY_EGG_ACCOUNT_NUMBER')
        self.assertRaises(ImproperlyConfigured, CrazyEggService)

    def test_wrong_id(self):
        self.settings_manager.set(CRAZY_EGG_ACCOUNT_NUMBER='1234567')
        self.assertRaises(ImproperlyConfigured, CrazyEggService)
        self.settings_manager.set(CRAZY_EGG_ACCOUNT_NUMBER='123456789')
        self.assertRaises(ImproperlyConfigured, CrazyEggService)

    def test_rendering(self):
        r = self.service.render_body_bottom({})
        self.assertTrue('/1234/5678.js' in r, r)

"""
Tests for the KISSinsights service.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.kissinsights import KissInsightsService
from analytical.tests.utils import TestSettingsManager


class KissInsightsTestCase(TestCase):
    """
    Tests for the KISSinsights service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(KISSINSIGHTS_ACCOUNT_NUMBER='12345')
        self.settings_manager.set(KISSINSIGHTS_SITE_CODE='abc')
        self.service = KissInsightsService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_top({}), "")
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_bottom({}), "")

    def test_no_account_number(self):
        self.settings_manager.delete('KISSINSIGHTS_ACCOUNT_NUMBER')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_no_site_code(self):
        self.settings_manager.delete('KISSINSIGHTS_SITE_CODE')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_wrong_account_number(self):
        self.settings_manager.set(KISSINSIGHTS_ACCOUNT_NUMBER='1234')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)
        self.settings_manager.set(KISSINSIGHTS_ACCOUNT_NUMBER='123456')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_wrong_site_id(self):
        self.settings_manager.set(KISSINSIGHTS_SITE_CODE='ab')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)
        self.settings_manager.set(KISSINSIGHTS_SITE_CODE='abcd')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_rendering(self):
        r = self.service.render_body_top({})
        self.assertTrue("//s3.amazonaws.com/ki.js/12345/abc.js" in r, r)

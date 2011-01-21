"""
Tests for the Google Analytics service.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.google_analytics import GoogleAnalyticsService
from analytical.tests.utils import TestSettingsManager


class GoogleAnalyticsTestCase(TestCase):
    """
    Tests for the Google Analytics service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7')
        self.service = GoogleAnalyticsService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_top({}), "")
        self.assertEqual(self.service.render_body_top({}), "")
        self.assertEqual(self.service.render_body_bottom({}), "")

    def test_no_property_id(self):
        self.settings_manager.delete('GOOGLE_ANALYTICS_PROPERTY_ID')
        self.assertRaises(ImproperlyConfigured, GoogleAnalyticsService)

    def test_wrong_id(self):
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='wrong')
        self.assertRaises(ImproperlyConfigured, GoogleAnalyticsService)

    def test_rendering(self):
        r = self.service.render_head_bottom({})
        self.assertTrue("_gaq.push(['_setAccount', 'UA-123456-7']);" in r, r)

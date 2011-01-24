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

    def test_wrong_property_id(self):
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='wrong')
        self.assertRaises(ImproperlyConfigured, GoogleAnalyticsService)

    def test_rendering(self):
        r = self.service.render_head_bottom({})
        self.assertTrue("_gaq.push(['_setAccount', 'UA-123456-7']);" in r, r)
        self.assertTrue("_gaq.push(['_trackPageview']);" in r, r)

    def test_custom_vars(self):
        context = {'google_analytics_custom_vars': [
            (1, 'test1', 'foo'),
            (5, 'test2', 'bar', 1),
        ]}
        r = self.service.render_head_bottom(context)
        self.assertTrue("_gaq.push(['_setCustomVar', 1, 'test1', 'foo', 2]);"
                in r, r)
        self.assertTrue("_gaq.push(['_setCustomVar', 5, 'test2', 'bar', 1]);"
                in r, r)
        self.assertRaises(ValueError, self.service.render_head_bottom,
                {'google_analytics_custom_vars': [(0, 'test', 'test')]})
        self.assertRaises(ValueError, self.service.render_head_bottom,
                {'google_analytics_custom_vars': [(6, 'test', 'test')]})

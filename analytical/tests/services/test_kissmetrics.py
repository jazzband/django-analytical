"""
Tests for the KISSmetrics service.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.kissmetrics import KissMetricsService
from analytical.tests.utils import TestSettingsManager


class KissMetricsTestCase(TestCase):
    """
    Tests for the KISSmetrics service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(KISSMETRICS_API_KEY='0123456789abcdef0123456'
                '789abcdef01234567')
        self.service = KissMetricsService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_top({}), "")
        self.assertEqual(self.service.render_body_bottom({}), "")

    def test_no_api_key(self):
        self.settings_manager.delete('KISSMETRICS_API_KEY')
        self.assertRaises(ImproperlyConfigured, KissMetricsService)

    def test_wrong_api_key(self):
        self.settings_manager.set(KISSMETRICS_API_KEY='0123456789abcdef0123456'
                '789abcdef0123456')
        self.assertRaises(ImproperlyConfigured, KissMetricsService)
        self.settings_manager.set(KISSMETRICS_API_KEY='0123456789abcdef0123456'
                '789abcdef012345678')
        self.assertRaises(ImproperlyConfigured, KissMetricsService)

    def test_rendering(self):
        r = self.service.render_head_top({})
        self.assertTrue("//doug1izaerwt3.cloudfront.net/0123456789abcdef012345"
                "6789abcdef01234567.1.js" in r, r)

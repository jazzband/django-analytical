"""
Tests for the Optimizely service.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.optimizely import OptimizelyService
from analytical.tests.utils import TestSettingsManager


class OptimizelyTestCase(TestCase):
    """
    Tests for the Optimizely service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='1234567')
        self.service = OptimizelyService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_top({}), "")
        self.assertEqual(self.service.render_body_bottom({}), "")

    def test_no_account_number(self):
        self.settings_manager.delete('OPTIMIZELY_ACCOUNT_NUMBER')
        self.assertRaises(ImproperlyConfigured, OptimizelyService)

    def test_wrong_account_number(self):
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='123456')
        self.assertRaises(ImproperlyConfigured, OptimizelyService)
        self.settings_manager.set(OPTIMIZELY_ACCOUNT_NUMBER='12345678')
        self.assertRaises(ImproperlyConfigured, OptimizelyService)

    def test_rendering(self):
        self.assertEqual(self.service.render_head_top({}),
                '<script src="//cdn.optimizely.com/js/1234567.js"></script>')

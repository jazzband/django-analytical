"""
Tests for the services package.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical import services
from analytical.services import load_services
from analytical.tests.utils import TestSettingsManager
from analytical.services.google_analytics import GoogleAnalyticsService


class GetEnabledServicesTestCase(TestCase):
    """
    Tests for get_enabled_services.
    """

    def setUp(self):
        services.enabled_services = None
        services.load_services = self._dummy_load_services_1

    def tearDown(self):
        services.load_services = load_services

    def test_no_reload(self):
        result = services.get_enabled_services()
        self.assertEqual(result, 'test1')
        services.load_services = self._dummy_load_services_2
        result = services.get_enabled_services()
        self.assertEqual(result, 'test1')

    def test_reload(self):
        result = services.get_enabled_services()
        self.assertEqual(result, 'test1')
        services.load_services = self._dummy_load_services_2
        result = services.get_enabled_services(reload=True)
        self.assertEqual(result, 'test2')

    def _dummy_load_services_1(self):
        return 'test1'

    def _dummy_load_services_2(self):
        return 'test2'


class LoadServicesTestCase(TestCase):
    """
    Tests for load_services.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.delete('ANALYTICAL_SERVICES')
        self.settings_manager.delete('CLICKY_SITE_ID')
        self.settings_manager.delete('CRAZY_EGG_ACCOUNT_NUMBER')
        self.settings_manager.delete('GOOGLE_ANALYTICS_PROPERTY_ID')
        self.settings_manager.delete('KISSINSIGHTS_ACCOUNT_NUMBER')
        self.settings_manager.delete('KISSINSIGHTS_SITE_CODE')
        self.settings_manager.delete('KISSMETRICS_API_KEY')
        self.settings_manager.delete('MIXPANEL_TOKEN')
        self.settings_manager.delete('OPTIMIZELY_ACCOUNT_NUMBER')

    def tearDown(self):
        self.settings_manager.revert()

    def test_no_services(self):
        self.assertEqual(load_services(), [])

    def test_enabled_service(self):
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='UA-1234567-8')
        results = load_services()
        self.assertEqual(len(results), 1, results)
        self.assertTrue(isinstance(results[0], GoogleAnalyticsService),
                results)

    def test_explicit_service(self):
        self.settings_manager.set(ANALYTICAL_SERVICES=[
                'analytical.services.google_analytics.GoogleAnalyticsService'])
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='UA-1234567-8')
        results = load_services()
        self.assertEqual(len(results), 1, results)
        self.assertTrue(isinstance(results[0], GoogleAnalyticsService),
                results)

    def test_explicit_service_misconfigured(self):
        self.settings_manager.set(ANALYTICAL_SERVICES=[
                'analytical.services.google_analytics.GoogleAnalyticsService'])
        self.assertRaises(ImproperlyConfigured, load_services)

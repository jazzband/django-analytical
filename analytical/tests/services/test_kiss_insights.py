"""
Tests for the KISSinsights service.
"""

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.kiss_insights import KissInsightsService
from analytical.tests.utils import TestSettingsManager


class KissInsightsTestCase(TestCase):
    """
    Tests for the KISSinsights service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(KISS_INSIGHTS_ACCOUNT_NUMBER='12345')
        self.settings_manager.set(KISS_INSIGHTS_SITE_CODE='abc')
        self.service = KissInsightsService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_top({}), "")
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_bottom({}), "")

    def test_no_account_number(self):
        self.settings_manager.delete('KISS_INSIGHTS_ACCOUNT_NUMBER')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_no_site_code(self):
        self.settings_manager.delete('KISS_INSIGHTS_SITE_CODE')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_wrong_account_number(self):
        self.settings_manager.set(KISS_INSIGHTS_ACCOUNT_NUMBER='1234')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)
        self.settings_manager.set(KISS_INSIGHTS_ACCOUNT_NUMBER='123456')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_wrong_site_id(self):
        self.settings_manager.set(KISS_INSIGHTS_SITE_CODE='ab')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)
        self.settings_manager.set(KISS_INSIGHTS_SITE_CODE='abcd')
        self.assertRaises(ImproperlyConfigured, KissInsightsService)

    def test_rendering(self):
        r = self.service.render_body_top({})
        self.assertTrue("//s3.amazonaws.com/ki.js/12345/abc.js" in r, r)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = self.service.render_body_top({'user': User(username='test')})
        self.assertTrue("_kiq.push(['identify', 'test']);" in r, r)

    def test_show_survey(self):
        r = self.service.render_body_top({'kiss_insights_show_survey': 1234})
        self.assertTrue("_kiq.push(['showSurvey', 1234]);" in r, r)

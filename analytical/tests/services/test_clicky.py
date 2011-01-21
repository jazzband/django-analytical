"""
Tests for the Clicky service.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from analytical.services.clicky import ClickyService
from analytical.tests.utils import TestSettingsManager


class ClickyTestCase(TestCase):
    """
    Tests for the Clicky service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(CLICKY_SITE_ID='12345678')
        self.service = ClickyService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_top({}), "")
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_top({}), "")

    def test_no_site_id(self):
        self.settings_manager.delete('CLICKY_SITE_ID')
        self.assertRaises(ImproperlyConfigured, ClickyService)

    def test_wrong_id(self):
        self.settings_manager.set(CLICKY_SITE_ID='1234567')
        self.assertRaises(ImproperlyConfigured, ClickyService)
        self.settings_manager.set(CLICKY_SITE_ID='123456789')
        self.assertRaises(ImproperlyConfigured, ClickyService)

    def test_rendering(self):
        r = self.service.render_body_bottom({})
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertTrue('src="http://in.getclicky.com/12345678ns.gif"' in r,
                r)

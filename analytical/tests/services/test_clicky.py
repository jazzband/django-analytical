"""
Tests for the Clicky service.
"""

import re

from django.contrib.auth.models import User
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

    def test_wrong_site_id(self):
        self.settings_manager.set(CLICKY_SITE_ID='1234567')
        self.assertRaises(ImproperlyConfigured, ClickyService)
        self.settings_manager.set(CLICKY_SITE_ID='123456789')
        self.assertRaises(ImproperlyConfigured, ClickyService)

    def test_rendering(self):
        r = self.service.render_body_bottom({})
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertTrue('src="http://in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = self.service.render_body_bottom({'user': User(username='test')})
        self.assertTrue(
                'var clicky_custom = {"session": {"username": "test"}};' in r,
                r)

    def test_custom(self):
        custom = {'var1': 'val1', 'var2': 'val2'}
        r = self.service.render_body_bottom({'clicky_custom': custom})
        self.assertTrue(re.search('var clicky_custom = {.*'
                '"var1": "val1", "var2": "val2".*};', r), r)

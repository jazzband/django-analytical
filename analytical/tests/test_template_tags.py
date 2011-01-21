"""
Tests for the template tags.
"""

from django.test import TestCase

from analytical.tests.utils import TestSettingsManager


class TemplateTagsTestCase(TestCase):
    """
    Tests for the template tags.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()

    def tearDown(self):
        self.settings_manager.revert()

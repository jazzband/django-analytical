"""
Tests for the console debugging service.
"""

from django.test import TestCase

from analytical.services.console import ConsoleService


class ConsoleTestCase(TestCase):
    """
    Tests for the console debugging service.
    """

    def setUp(self):
        self.service = ConsoleService()

    def test_render_head_top(self):
        r = self.service.render_head_top({})
        self.assertTrue('rendering analytical_head_top tag' in r, r)

    def test_render_head_bottom(self):
        r = self.service.render_head_bottom({})
        self.assertTrue('rendering analytical_head_bottom tag' in r, r)

    def test_render_body_top(self):
        r = self.service.render_body_top({})
        self.assertTrue('rendering analytical_body_top tag' in r, r)

    def test_render_body_bottom(self):
        r = self.service.render_body_bottom({})
        self.assertTrue('rendering analytical_body_bottom tag' in r, r)

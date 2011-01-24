"""
Tests for the template tags.
"""

from django.http import HttpRequest
from django import template
from django.test import TestCase

from analytical import services
from analytical.tests.utils import TestSettingsManager


class TemplateTagsTestCase(TestCase):
    """
    Tests for the template tags.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(ANALYTICAL_SERVICES=[
                'analytical.services.console.ConsoleService'])
        services.enabled_services = None

    def tearDown(self):
        self.settings_manager.revert()
        services.enabled_services = None

    def render_location_tag(self, location, context=None):
        if context is None: context = {}
        t = template.Template(
                "{%% load analytical %%}{%% analytical_setup_%s %%}"
                % location)
        return t.render(template.Context(context))

    def test_location_tags(self):
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(l)
            self.assertTrue('rendering analytical_%s tag' % l in r, r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(l, {'request': req})
            self.assertTrue('<!-- Analytical disabled on internal IP address'
                    in r, r)

    def test_render_internal_ip_fallback(self):
        self.settings_manager.set(INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(l, {'request': req})
            self.assertTrue('<!-- Analytical disabled on internal IP address'
                    in r, r)

    def test_render_internal_ip_forwarded_for(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['HTTP_X_FORWARDED_FOR'] = '1.1.1.1'
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(l, {'request': req})
            self.assertTrue('<!-- Analytical disabled on internal IP address'
                    in r, r)

    def test_render_different_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '2.2.2.2'
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(l, {'request': req})
            self.assertFalse('<!-- Analytical disabled on internal IP address'
                    in r, r)

    def test_render_internal_ip_empty(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        self.settings_manager.delete('ANALYTICAL_SERVICES')
        self.settings_manager.delete('CLICKY_SITE_ID')
        self.settings_manager.delete('CRAZY_EGG_ACCOUNT_NUMBER')
        self.settings_manager.delete('GOOGLE_ANALYTICS_PROPERTY_ID')
        self.settings_manager.delete('KISSINSIGHTS_ACCOUNT_NUMBER')
        self.settings_manager.delete('KISSINSIGHTS_SITE_CODE')
        self.settings_manager.delete('KISSMETRICS_API_KEY')
        self.settings_manager.delete('MIXPANEL_TOKEN')
        self.settings_manager.delete('OPTIMIZELY_ACCOUNT_NUMBER')
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            self.assertEqual(self.render_location_tag(l, {'request': req}), "")

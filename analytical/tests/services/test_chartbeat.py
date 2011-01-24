"""
Tests for the Chartbeat service.
"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.test import TestCase

from analytical.services.chartbeat import ChartbeatService
from analytical.tests.utils import TestSettingsManager


class ChartbeatTestCase(TestCase):
    """
    Tests for the Chartbeat service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.settings_manager.set(CHARTBEAT_USER_ID='12345')
        self.service = ChartbeatService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_empty_locations(self):
        self.assertEqual(self.service.render_head_bottom({}), "")
        self.assertEqual(self.service.render_body_top({}), "")

    def test_no_user_id(self):
        self.settings_manager.delete('CHARTBEAT_USER_ID')
        self.assertRaises(ImproperlyConfigured, ChartbeatService)

    def test_wrong_user_id(self):
        self.settings_manager.set(CHARTBEAT_USER_ID='1234')
        self.assertRaises(ImproperlyConfigured, ChartbeatService)
        self.settings_manager.set(CHARTBEAT_USER_ID='123456')
        self.assertRaises(ImproperlyConfigured, ChartbeatService)

    def test_rendering_init(self):
        r = self.service.render_head_top({})
        self.assertTrue('var _sf_startpt=(new Date()).getTime()' in r, r)

    def test_rendering_setup(self):
        r = self.service.render_body_bottom({'chartbeat_domain': "test.com"})
        self.assertTrue('var _sf_async_config={uid:12345,domain:"test.com"};'
                in r, r)

    def test_rendering_setup_request_domain(self):
        req = HttpRequest()
        req.META['HTTP_HOST'] = 'test.com'
        r = self.service.render_body_bottom({'request': req})
        self.assertTrue('var _sf_async_config={uid:12345,domain:"test.com"};'
                in r, r)

    def test_rendering_setup_site(self):
        installed_apps = list(settings.INSTALLED_APPS)
        installed_apps.append('django.contrib.sites')
        self.settings_manager.set(INSTALLED_APPS=installed_apps)
        site = Site.objects.create(domain="test.com", name="test")
        self.settings_manager.set(SITE_ID=site.id)
        r = self.service.render_body_bottom({})
        self.assertTrue('var _sf_async_config={uid:12345,domain:"test.com"};'
                in r, r)

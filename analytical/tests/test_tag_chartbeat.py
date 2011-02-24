"""
Tests for the Chartbeat template tags and filters.
"""

import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.chartbeat import ChartbeatTopNode, \
        ChartbeatBottomNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class ChartbeatTagTestCase(TagTestCase):
    """
    Tests for the ``chartbeat`` template tag.
    """

    def setUp(self):
        super(ChartbeatTagTestCase, self).setUp()
        self.settings_manager.set(CHARTBEAT_USER_ID='12345')

    def test_top_tag(self):
        r = self.render_tag('chartbeat', 'chartbeat_top',
                {'chartbeat_domain': "test.com"})
        self.assertTrue('var _sf_startpt=(new Date()).getTime()' in r, r)

    def test_bottom_tag(self):
        r = self.render_tag('chartbeat', 'chartbeat_bottom',
                {'chartbeat_domain': "test.com"})
        self.assertTrue(re.search(
                'var _sf_async_config={.*"uid": "12345".*};', r), r)
        self.assertTrue(re.search(
                'var _sf_async_config={.*"domain": "test.com".*};', r), r)

    def test_top_node(self):
        r = ChartbeatTopNode().render(
                Context({'chartbeat_domain': "test.com"}))
        self.assertTrue('var _sf_startpt=(new Date()).getTime()' in r, r)

    def test_bottom_node(self):
        r = ChartbeatBottomNode().render(
                Context({'chartbeat_domain': "test.com"}))
        self.assertTrue(re.search(
                'var _sf_async_config={.*"uid": "12345".*};', r), r)
        self.assertTrue(re.search(
                'var _sf_async_config={.*"domain": "test.com".*};', r), r)

    def test_no_user_id(self):
        self.settings_manager.delete('CHARTBEAT_USER_ID')
        self.assertRaises(AnalyticalException, ChartbeatBottomNode)

    def test_wrong_user_id(self):
        self.settings_manager.set(CHARTBEAT_USER_ID='123abc')
        self.assertRaises(AnalyticalException, ChartbeatBottomNode)

    def test_rendering_setup_no_site(self):
        installed_apps = [a for a in settings.INSTALLED_APPS
                if a != 'django.contrib.sites']
        self.settings_manager.set(INSTALLED_APPS=installed_apps)
        r = ChartbeatBottomNode().render(Context())
        self.assertTrue('var _sf_async_config={"uid": "12345"};' in r, r)

    def test_rendering_setup_site(self):
        installed_apps = list(settings.INSTALLED_APPS)
        installed_apps.append('django.contrib.sites')
        self.settings_manager.set(INSTALLED_APPS=installed_apps)
        site = Site.objects.create(domain="test.com", name="test")
        self.settings_manager.set(SITE_ID=site.id)
        r = ChartbeatBottomNode().render(Context())
        self.assertTrue(re.search(
                'var _sf_async_config={.*"uid": "12345".*};', r), r)
        self.assertTrue(re.search(
                'var _sf_async_config={.*"domain": "test.com".*};', r), r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ChartbeatBottomNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Chartbeat disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

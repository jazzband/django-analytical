"""
Tests for the Chartbeat template tags and filters.
"""

import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.template import Context
from django.test import TestCase

from analytical.templatetags.chartbeat import ChartbeatTopNode, \
        ChartbeatBottomNode
from analytical.tests.utils import TagTestCase, with_apps, without_apps, \
        override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@without_apps('django.contrib.sites')
@override_settings(CHARTBEAT_USER_ID='12345')
class ChartbeatTagTestCaseNoSites(TestCase):
    def test_rendering_setup_no_site(self):
        r = ChartbeatBottomNode().render(Context())
        self.assertTrue('var _sf_async_config={"uid": "12345"};' in r, r)


@with_apps('django.contrib.sites')
@override_settings(CHARTBEAT_USER_ID='12345')
class ChartbeatTagTestCaseWithSites(TestCase):
    def setUp(self):
        from django.core.management import call_command
        from django.db.models import loading
        loading.cache.loaded = False
        call_command("syncdb", verbosity=0)

    def test_rendering_setup_site(self):
        site = Site.objects.create(domain="test.com", name="test")
        with override_settings(SITE_ID=site.id):
            r = ChartbeatBottomNode().render(Context())
            self.assertTrue(re.search(
                    'var _sf_async_config={.*"uid": "12345".*};', r), r)
            self.assertTrue(re.search(
                    'var _sf_async_config={.*"domain": "test.com".*};', r), r)

    @override_settings(CHARTBEAT_AUTO_DOMAIN=False)
    def test_auto_domain_false(self):
        """
        Even if 'django.contrib.sites' is in INSTALLED_APPS, if
        CHARTBEAT_AUTO_DOMAIN is False, ensure there is no 'domain'
        in _sf_async_config.
        """
        r = ChartbeatBottomNode().render(Context())
        self.assertTrue('var _sf_async_config={"uid": "12345"};' in r, r)


@override_settings(CHARTBEAT_USER_ID='12345')
class ChartbeatTagTestCase(TagTestCase):
    """
    Tests for the ``chartbeat`` template tag.
    """

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

    @override_settings(CHARTBEAT_USER_ID=SETTING_DELETED)
    def test_no_user_id(self):
        self.assertRaises(AnalyticalException, ChartbeatBottomNode)

    @override_settings(CHARTBEAT_USER_ID='123abc')
    def test_wrong_user_id(self):
        self.assertRaises(AnalyticalException, ChartbeatBottomNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ChartbeatBottomNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Chartbeat disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

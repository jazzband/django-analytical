"""
Tests for the Google Analytics template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.google_analytics import GoogleAnalyticsNode, \
        TRACK_SINGLE_DOMAIN, TRACK_MULTIPLE_DOMAINS, TRACK_MULTIPLE_SUBDOMAINS,\
        SCOPE_VISITOR, SCOPE_SESSION, SCOPE_PAGE
from analytical.tests.utils import TestCase, TagTestCase, override_settings, \
        without_apps, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7',
        GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_SINGLE_DOMAIN)
class GoogleAnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``google_analytics`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('google_analytics', 'google_analytics')
        self.assertTrue("_gaq.push(['_setAccount', 'UA-123456-7']);" in r, r)
        self.assertTrue("_gaq.push(['_trackPageview']);" in r, r)

    def test_node(self):
        r = GoogleAnalyticsNode().render(Context())
        self.assertTrue("_gaq.push(['_setAccount', 'UA-123456-7']);" in r, r)
        self.assertTrue("_gaq.push(['_trackPageview']);" in r, r)

    @override_settings(GOOGLE_ANALYTICS_PROPERTY_ID=SETTING_DELETED)
    def test_no_property_id(self):
        self.assertRaises(AnalyticalException, GoogleAnalyticsNode)

    @override_settings(GOOGLE_ANALYTICS_PROPERTY_ID='wrong')
    def test_wrong_property_id(self):
        self.assertRaises(AnalyticalException, GoogleAnalyticsNode)

    @override_settings(
            GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_SUBDOMAINS,
            GOOGLE_ANALYTICS_DOMAIN='example.com')
    def test_track_multiple_subdomains(self):
        r = GoogleAnalyticsNode().render(Context())
        self.assertTrue("_gaq.push(['_setDomainName', 'example.com']);" in r, r)
        self.assertTrue("_gaq.push(['_setAllowHash', false]);" in r, r)

    @override_settings(GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_DOMAINS,
            GOOGLE_ANALYTICS_DOMAIN='example.com')
    def test_track_multiple_domains(self):
        r = GoogleAnalyticsNode().render(Context())
        self.assertTrue("_gaq.push(['_setDomainName', 'example.com']);" in r, r)
        self.assertTrue("_gaq.push(['_setAllowHash', false]);" in r, r)
        self.assertTrue("_gaq.push(['_setAllowLinker', true]);" in r, r)

    def test_custom_vars(self):
        context = Context({
            'google_analytics_var1': ('test1', 'foo'),
            'google_analytics_var2': ('test2', 'bar', SCOPE_VISITOR),
            'google_analytics_var4': ('test4', 'baz', SCOPE_SESSION),
            'google_analytics_var5': ('test5', 'qux', SCOPE_PAGE),
        })
        r = GoogleAnalyticsNode().render(context)
        self.assertTrue("_gaq.push(['_setCustomVar', 1, 'test1', 'foo', 3]);"
                in r, r)
        self.assertTrue("_gaq.push(['_setCustomVar', 2, 'test2', 'bar', 1]);"
                in r, r)
        self.assertTrue("_gaq.push(['_setCustomVar', 4, 'test4', 'baz', 2]);"
                in r, r)
        self.assertTrue("_gaq.push(['_setCustomVar', 5, 'test5', 'qux', 3]);"
                in r, r)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED=True)
    def test_track_page_load_time(self):
        r = GoogleAnalyticsNode().render(Context())
        self.assertTrue("_gaq.push(['_trackPageLoadTime']);" in r, r)
        
    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Google Analytics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)


@without_apps('django.contrib.sites')
@override_settings(GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7',
        GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_DOMAINS,
        GOOGLE_ANALYTICS_DOMAIN=SETTING_DELETED,
        ANALYTICAL_DOMAIN=SETTING_DELETED)
class NoDomainTestCase(TestCase):
    def test_exception_without_domain(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsNode().render,
                context)
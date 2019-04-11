"""
Tests for the Google Analytics template tags and filters, using the new analytics.js library.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.google_analytics_js import GoogleAnalyticsJsNode, \
    TRACK_SINGLE_DOMAIN, TRACK_MULTIPLE_DOMAINS, TRACK_MULTIPLE_SUBDOMAINS
from analytical.tests.utils import TestCase, TagTestCase
from analytical.utils import AnalyticalException


@override_settings(GOOGLE_ANALYTICS_JS_PROPERTY_ID='UA-123456-7',
                   GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_SINGLE_DOMAIN)
class GoogleAnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``google_analytics_js`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('google_analytics_js', 'google_analytics_js')
        self.assertTrue("""(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');""" in r, r)
        self.assertTrue("ga('create', 'UA-123456-7', 'auto', {});" in r, r)
        self.assertTrue("ga('send', 'pageview');" in r, r)

    def test_node(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue("""(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');""" in r, r)
        self.assertTrue("ga('create', 'UA-123456-7', 'auto', {});" in r, r)
        self.assertTrue("ga('send', 'pageview');" in r, r)

    @override_settings(GOOGLE_ANALYTICS_JS_PROPERTY_ID=None)
    def test_no_property_id(self):
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode)

    @override_settings(GOOGLE_ANALYTICS_JS_PROPERTY_ID='wrong')
    def test_wrong_property_id(self):
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode)

    @override_settings(GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_SUBDOMAINS,
                       GOOGLE_ANALYTICS_DOMAIN='example.com')
    def test_track_multiple_subdomains(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue(
            """ga('create', 'UA-123456-7', 'auto', {"legacyCookieDomain": "example.com"}""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_DOMAINS,
                       GOOGLE_ANALYTICS_DOMAIN='example.com')
    def test_track_multiple_domains(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue("ga('create', 'UA-123456-7', 'auto', {" in r, r)
        self.assertTrue('"legacyCookieDomain": "example.com"' in r, r)
        self.assertTrue('"allowLinker\": true' in r, r)

    def test_custom_vars(self):
        context = Context({
            'google_analytics_var1': ('test1', 'foo'),
            'google_analytics_var2': ('test2', 'bar'),
            'google_analytics_var4': ('test4', 1),
            'google_analytics_var5': ('test5', 2.2),
        })
        r = GoogleAnalyticsJsNode().render(context)
        self.assertTrue("ga('set', 'test1', 'foo');" in r, r)
        self.assertTrue("ga('set', 'test2', 'bar');" in r, r)
        self.assertTrue("ga('set', 'test4', 1);" in r, r)
        self.assertTrue("ga('set', 'test5', 2.2);" in r, r)

    def test_display_advertising(self):
        with override_settings(GOOGLE_ANALYTICS_DISPLAY_ADVERTISING=True):
            r = GoogleAnalyticsJsNode().render(Context())
            self.assertTrue("""ga('create', 'UA-123456-7', 'auto', {});
ga('require', 'displayfeatures');
ga('send', 'pageview');""" in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsJsNode().render(context)
        self.assertTrue(r.startswith(
            '<!-- Google Analytics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

    @override_settings(GOOGLE_ANALYTICS_ANONYMIZE_IP=True)
    def test_anonymize_ip(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue("ga('set', 'anonymizeIp', true);" in r, r)

    @override_settings(GOOGLE_ANALYTICS_ANONYMIZE_IP=False)
    def test_anonymize_ip_not_present(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertFalse("ga('set', 'anonymizeIp', true);" in r, r)

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE=0.0)
    def test_set_sample_rate_min(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue("""ga('create', 'UA-123456-7', 'auto', {"sampleRate": 0});""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE='100.00')
    def test_set_sample_rate_max(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue("""ga('create', 'UA-123456-7', 'auto', {"sampleRate": 100});""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE=-1)
    def test_exception_whenset_sample_rate_too_small(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode().render, context)

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE=101)
    def test_exception_when_set_sample_rate_too_large(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode().render, context)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE=0.0)
    def test_set_site_speed_sample_rate_min(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue(
            """ga('create', 'UA-123456-7', 'auto', {"siteSpeedSampleRate": 0});""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE='100.00')
    def test_set_site_speed_sample_rate_max(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue(
            """ga('create', 'UA-123456-7', 'auto', {"siteSpeedSampleRate": 100});""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE=-1)
    def test_exception_whenset_site_speed_sample_rate_too_small(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode().render, context)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE=101)
    def test_exception_when_set_site_speed_sample_rate_too_large(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode().render, context)

    @override_settings(GOOGLE_ANALYTICS_COOKIE_EXPIRATION=0)
    def test_set_cookie_expiration_min(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue("""ga('create', 'UA-123456-7', 'auto', {"cookieExpires": 0});""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_COOKIE_EXPIRATION='10000')
    def test_set_cookie_expiration_as_string(self):
        r = GoogleAnalyticsJsNode().render(Context())
        self.assertTrue(
            """ga('create', 'UA-123456-7', 'auto', {"cookieExpires": 10000});""" in r, r)

    @override_settings(GOOGLE_ANALYTICS_COOKIE_EXPIRATION=-1)
    def test_exception_when_set_cookie_expiration_too_small(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode().render, context)


@override_settings(GOOGLE_ANALYTICS_JS_PROPERTY_ID='UA-123456-7',
                   GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_DOMAINS,
                   GOOGLE_ANALYTICS_DOMAIN=None,
                   ANALYTICAL_DOMAIN=None)
class NoDomainTestCase(TestCase):
    def test_exception_without_domain(self):
        context = Context()
        self.assertRaises(AnalyticalException, GoogleAnalyticsJsNode().render, context)

"""
Tests for the Google Analytics template tags and filters.
"""

import pytest
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase, TestCase

from analytical.templatetags.google_analytics import (
    SCOPE_PAGE,
    SCOPE_SESSION,
    SCOPE_VISITOR,
    TRACK_MULTIPLE_DOMAINS,
    TRACK_MULTIPLE_SUBDOMAINS,
    TRACK_SINGLE_DOMAIN,
    GoogleAnalyticsNode,
)
from analytical.utils import AnalyticalException


@override_settings(
    GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7',
    GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_SINGLE_DOMAIN,
)
class GoogleAnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``google_analytics`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('google_analytics', 'google_analytics')
        assert "_gaq.push(['_setAccount', 'UA-123456-7']);" in r
        assert "_gaq.push(['_trackPageview']);" in r

    def test_node(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setAccount', 'UA-123456-7']);" in r
        assert "_gaq.push(['_trackPageview']);" in r

    @override_settings(GOOGLE_ANALYTICS_PROPERTY_ID=None)
    def test_no_property_id(self):
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode()

    @override_settings(GOOGLE_ANALYTICS_PROPERTY_ID='wrong')
    def test_wrong_property_id(self):
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode()

    @override_settings(
        GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_SUBDOMAINS,
        GOOGLE_ANALYTICS_DOMAIN='example.com',
    )
    def test_track_multiple_subdomains(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setDomainName', 'example.com']);" in r
        assert "_gaq.push(['_setAllowHash', false]);" in r

    @override_settings(
        GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_DOMAINS,
        GOOGLE_ANALYTICS_DOMAIN='example.com',
    )
    def test_track_multiple_domains(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setDomainName', 'example.com']);" in r
        assert "_gaq.push(['_setAllowHash', false]);" in r
        assert "_gaq.push(['_setAllowLinker', true]);" in r

    def test_custom_vars(self):
        context = Context(
            {
                'google_analytics_var1': ('test1', 'foo'),
                'google_analytics_var2': ('test2', 'bar', SCOPE_VISITOR),
                'google_analytics_var4': ('test4', 'baz', SCOPE_SESSION),
                'google_analytics_var5': ('test5', 'qux', SCOPE_PAGE),
            }
        )
        r = GoogleAnalyticsNode().render(context)
        assert "_gaq.push(['_setCustomVar', 1, 'test1', 'foo', 3]);" in r
        assert "_gaq.push(['_setCustomVar', 2, 'test2', 'bar', 1]);" in r
        assert "_gaq.push(['_setCustomVar', 4, 'test4', 'baz', 2]);" in r
        assert "_gaq.push(['_setCustomVar', 5, 'test5', 'qux', 3]);" in r

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED=True)
    def test_track_page_load_time(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_trackPageLoadTime']);" in r

    def test_display_advertising(self):
        with override_settings(GOOGLE_ANALYTICS_DISPLAY_ADVERTISING=False):
            r = GoogleAnalyticsNode().render(Context())
            assert 'google-analytics.com/ga.js' in r
        with override_settings(GOOGLE_ANALYTICS_DISPLAY_ADVERTISING=True):
            r = GoogleAnalyticsNode().render(Context())
            assert 'stats.g.doubleclick.net/dc.js' in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsNode().render(context)
        assert r.startswith('<!-- Google Analytics disabled on internal IP address')
        assert r.endswith('-->')

    @override_settings(GOOGLE_ANALYTICS_ANONYMIZE_IP=True)
    def test_anonymize_ip(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_gat._anonymizeIp']);" in r
        assert r.index('_gat._anonymizeIp') < r.index('_trackPageview')

    @override_settings(GOOGLE_ANALYTICS_ANONYMIZE_IP=False)
    def test_anonymize_ip_not_present(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_gat._anonymizeIp']);" not in r

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE=0.0)
    def test_set_sample_rate_min(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setSampleRate', '0.00']);" in r

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE='100.00')
    def test_set_sample_rate_max(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setSampleRate', '100.00']);" in r

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE=-1)
    def test_exception_whenset_sample_rate_too_small(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)

    @override_settings(GOOGLE_ANALYTICS_SAMPLE_RATE=101)
    def test_exception_when_set_sample_rate_too_large(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE=0.0)
    def test_set_site_speed_sample_rate_min(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setSiteSpeedSampleRate', '0.00']);" in r

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE='100.00')
    def test_set_site_speed_sample_rate_max(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setSiteSpeedSampleRate', '100.00']);" in r

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE=-1)
    def test_exception_whenset_site_speed_sample_rate_too_small(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)

    @override_settings(GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE=101)
    def test_exception_when_set_site_speed_sample_rate_too_large(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)

    @override_settings(GOOGLE_ANALYTICS_SESSION_COOKIE_TIMEOUT=0)
    def test_set_session_cookie_timeout_min(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setSessionCookieTimeout', '0']);" in r

    @override_settings(GOOGLE_ANALYTICS_SESSION_COOKIE_TIMEOUT='10000')
    def test_set_session_cookie_timeout_as_string(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setSessionCookieTimeout', '10000']);" in r

    @override_settings(GOOGLE_ANALYTICS_SESSION_COOKIE_TIMEOUT=-1)
    def test_exception_when_set_session_cookie_timeout_too_small(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)

    @override_settings(GOOGLE_ANALYTICS_VISITOR_COOKIE_TIMEOUT=0)
    def test_set_visitor_cookie_timeout_min(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setVisitorCookieTimeout', '0']);" in r

    @override_settings(GOOGLE_ANALYTICS_VISITOR_COOKIE_TIMEOUT='10000')
    def test_set_visitor_cookie_timeout_as_string(self):
        r = GoogleAnalyticsNode().render(Context())
        assert "_gaq.push(['_setVisitorCookieTimeout', '10000']);" in r

    @override_settings(GOOGLE_ANALYTICS_VISITOR_COOKIE_TIMEOUT=-1)
    def test_exception_when_set_visitor_cookie_timeout_too_small(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)


@override_settings(
    GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7',
    GOOGLE_ANALYTICS_TRACKING_STYLE=TRACK_MULTIPLE_DOMAINS,
    GOOGLE_ANALYTICS_DOMAIN=None,
    ANALYTICAL_DOMAIN=None,
)
class NoDomainTestCase(TestCase):
    def test_exception_without_domain(self):
        context = Context()
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsNode().render(context)

"""
Tests for the Google Analytics template tags and filters, using the new gtag.js library.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.google_analytics_gtag import GoogleAnalyticsGTagNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='UA-123456-7')
class GoogleAnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``google_analytics_js`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('google_analytics_gtag', 'google_analytics_gtag')
        self.assertTrue(
            '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123456-7"></script>'
            in r, r)
        self.assertTrue("gtag('js', new Date());" in r, r)
        self.assertTrue("gtag('config', 'UA-123456-7');" in r, r)

    def test_node(self):
        r = GoogleAnalyticsGTagNode().render(Context())
        self.assertTrue(
            '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123456-7"></script>'
            in r, r)
        self.assertTrue("gtag('js', new Date());" in r, r)
        self.assertTrue("gtag('config', 'UA-123456-7');" in r, r)

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID=None)
    def test_no_property_id(self):
        self.assertRaises(AnalyticalException, GoogleAnalyticsGTagNode)

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='wrong')
    def test_wrong_property_id(self):
        self.assertRaises(AnalyticalException, GoogleAnalyticsGTagNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsGTagNode().render(context)
        self.assertTrue(r.startswith(
            '<!-- Google Analytics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

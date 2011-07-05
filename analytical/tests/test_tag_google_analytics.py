"""
Tests for the Google Analytics template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.google_analytics import GoogleAnalyticsNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7')
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

    def test_custom_vars(self):
        context = Context({'google_analytics_var1': ('test1', 'foo'),
                'google_analytics_var5': ('test2', 'bar', 1)})
        r = GoogleAnalyticsNode().render(context)
        self.assertTrue("_gaq.push(['_setCustomVar', 1, 'test1', 'foo', 3]);"
                in r, r)
        self.assertTrue("_gaq.push(['_setCustomVar', 5, 'test2', 'bar', 1]);"
                in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Google Analytics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

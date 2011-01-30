"""
Tests for the Google Analytics template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.google_analytics import GoogleAnalyticsNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class GoogleAnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``google_analytics`` template tag.
    """

    def setUp(self):
        super(GoogleAnalyticsTagTestCase, self).setUp()
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='UA-123456-7')

    def test_tag(self):
        r = self.render_tag('google_analytics', 'google_analytics')
        self.assertTrue("_gaq.push(['_setAccount', 'UA-123456-7']);" in r, r)
        self.assertTrue("_gaq.push(['_trackPageview']);" in r, r)

    def test_node(self):
        r = GoogleAnalyticsNode().render(Context())
        self.assertTrue("_gaq.push(['_setAccount', 'UA-123456-7']);" in r, r)
        self.assertTrue("_gaq.push(['_trackPageview']);" in r, r)

    def test_no_property_id(self):
        self.settings_manager.delete('GOOGLE_ANALYTICS_PROPERTY_ID')
        self.assertRaises(AnalyticalException, GoogleAnalyticsNode)

    def test_wrong_property_id(self):
        self.settings_manager.set(GOOGLE_ANALYTICS_PROPERTY_ID='wrong')
        self.assertRaises(AnalyticalException, GoogleAnalyticsNode)

    def test_custom_vars(self):
        context = Context({'google_analytics_var1': ('test1', 'foo'),
                'google_analytics_var5': ('test2', 'bar', 1)})
        r = GoogleAnalyticsNode().render(context)
        self.assertTrue("_gaq.push(['_setCustomVar', 1, 'test1', 'foo', 3]);"
                in r, r)
        self.assertTrue("_gaq.push(['_setCustomVar', 5, 'test2', 'bar', 1]);"
                in r, r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Google Analytics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

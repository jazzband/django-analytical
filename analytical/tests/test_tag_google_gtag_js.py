"""
Tests for the Google Analytics template tags and filters, using the new analytics.js library.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.google_gtag_js import GoogleGTagJsNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(GOOGLE_GTAG_JS_PROPERTY_ID='UA-123456-7')
class GoogleGTagJsTagTestCase(TagTestCase):
    """
    Tests for the ``google_gtag_js`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('google_gtag_js', 'google_gtag_js')
        self.assertTrue("""<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123456-7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());""" in r, r)
        self.assertTrue("gtag('config', 'UA-123456-7'" in r, r)

    def test_node(self):
        r = GoogleGTagJsNode().render(Context())
        self.assertTrue("""<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123456-7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());""" in r, r)
        self.assertTrue("gtag('config', 'UA-123456-7'" in r, r)

    @override_settings(GOOGLE_GTAG_JS_PROPERTY_ID=None)
    def test_no_property_id(self):
        self.assertRaises(AnalyticalException, GoogleGTagJsNode)

    def test_custom_set_vars(self):
        context = Context({
            'google_gtag_js_set1': ('test1', 'foo'),
            'google_gtag_js_set2': ('test2', 'bar'),
            'google_gtag_js_set4': ('test4', 1),
            'google_gtag_js_set5': ('test5', 2.2),
        })
        r = GoogleGTagJsNode().render(context)
        self.assertTrue("""gtag('set', 'test1', "foo");""" in r, r)
        self.assertTrue("""gtag('set', 'test2', "bar");""" in r, r)
        self.assertTrue("""gtag('set', 'test4', 1);""" in r, r)
        self.assertTrue("""gtag('set', 'test5', 2.2);""" in r, r)

    def test_custom_set_data(self):
        context = Context({
            'google_gtag_js_set_data': {'test1': 'foo'},
        })
        r = GoogleGTagJsNode().render(context)
        self.assertTrue("""gtag('set', {"test1": "foo"});""" in r, r)

    def test_custom_set_data_not_ignored(self):
        context = Context({
            'google_gtag_js_set_data': {'test1': 'foo'},
            'google_gtag_js_set2': ('test2', 'bar'),
        })
        r = GoogleGTagJsNode().render(context)
        self.assertTrue("""gtag('set', {"test1": "foo"});""" in r, r)
        self.assertTrue("""gtag('set', 'test2', "bar");""" in r, r)

    def test_custom_config_context_dic(self):
        context = Context({
            'google_gtag_js_config_data': {'test1': True},
            'google_gtag_js_set1': ('shouldnt_affect', 'config'),
        })
        r = GoogleGTagJsNode().render(context)
        self.assertTrue("""gtag('config', 'UA-123456-7', {"test1": true});""" in r, r)

    @override_settings(
        GOOGLE_GTAG_JS_DEFAULT_CONFIG={'test1': True},
    )
    def test_custom_config_defaults_dic(self):
        context = Context({
            'google_gtag_js_config_data': {},
        })
        r = GoogleGTagJsNode().render(context)
        self.assertTrue("""gtag('config', 'UA-123456-7', {"test1": true});""" in r, r)

    @override_settings(
        GOOGLE_GTAG_JS_DEFAULT_CONFIG={'test1': True},
    )
    def test_custom_config_context_overrides_defaults(self):
        context = Context({
            'google_gtag_js_config_data': {'test1': False},
        })
        r = GoogleGTagJsNode().render(context)
        self.assertTrue("""gtag('config', 'UA-123456-7', {"test1": false});""" in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleGTagJsNode().render(context)
        self.assertTrue(r.startswith(
            '<!-- Google Analytics disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

"""
Tests for the Piwik template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.piwik import PiwikNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(PIWIK_DOMAIN_PATH='example.com', PIWIK_SITE_ID='345')
class PiwikTagTestCase(TagTestCase):
    """
    Tests for the ``piwik`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('piwik', 'piwik')
        self.assertTrue(' ? "https" : "http") + "://example.com/";' in r, r)
        self.assertTrue("_paq.push(['setSiteId', 345]);" in r, r)
        self.assertTrue('img src="http://example.com/piwik.php?idsite=345"'
                        in r, r)

    def test_node(self):
        r = PiwikNode().render(Context({}))
        self.assertTrue(' ? "https" : "http") + "://example.com/";' in r, r)
        self.assertTrue("_paq.push(['setSiteId', 345]);" in r, r)
        self.assertTrue('img src="http://example.com/piwik.php?idsite=345"'
                        in r, r)

    @override_settings(PIWIK_DOMAIN_PATH='example.com/piwik',
                       PIWIK_SITE_ID='345')
    def test_domain_path_valid(self):
        r = self.render_tag('piwik', 'piwik')
        self.assertTrue(' ? "https" : "http") + "://example.com/piwik/";' in r,
                        r)

    @override_settings(PIWIK_DOMAIN_PATH=None)
    def test_no_domain(self):
        self.assertRaises(AnalyticalException, PiwikNode)

    @override_settings(PIWIK_SITE_ID=None)
    def test_no_siteid(self):
        self.assertRaises(AnalyticalException, PiwikNode)

    @override_settings(PIWIK_SITE_ID='x')
    def test_siteid_not_a_number(self):
        self.assertRaises(AnalyticalException, PiwikNode)

    @override_settings(PIWIK_DOMAIN_PATH='http://www.example.com')
    def test_domain_protocol_invalid(self):
        self.assertRaises(AnalyticalException, PiwikNode)

    @override_settings(PIWIK_DOMAIN_PATH='example.com/')
    def test_domain_slash_invalid(self):
        self.assertRaises(AnalyticalException, PiwikNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = PiwikNode().render(context)
        self.assertTrue(r.startswith(
            '<!-- Piwik disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

    def test_uservars(self):
        context = Context({'piwik_vars': [(1, 'foo', 'foo_val'),
                                          (2, 'bar', 'bar_val', 'page'),
                                          (3, 'spam', 'spam_val', 'visit')]})
        r = PiwikNode().render(context)
        msg = 'Incorrect Piwik custom variable rendering. Expected:\n%s\nIn:\n%s'
        for var_code in ['_paq.push([1, "foo", "foo_val", "page"]);',
                         '_paq.push([2, "bar", "bar_val", "page"]);',
                         '_paq.push([3, "spam", "spam_val", "visit"]);']:
            self.assertIn(var_code, r, msg % (var_code, r))

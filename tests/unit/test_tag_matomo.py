"""
Tests for the Matomo template tags and filters.
"""

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.matomo import MatomoNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(MATOMO_DOMAIN_PATH='example.com', MATOMO_SITE_ID='345')
class MatomoTagTestCase(TagTestCase):
    """
    Tests for the ``matomo`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('matomo', 'matomo')
        self.assertTrue('"//example.com/"' in r, r)
        self.assertTrue("_paq.push(['setSiteId', 345]);" in r, r)
        self.assertTrue('img src="//example.com/piwik.php?idsite=345"'
                        in r, r)

    def test_node(self):
        r = MatomoNode().render(Context({}))
        self.assertTrue('"//example.com/";' in r, r)
        self.assertTrue("_paq.push(['setSiteId', 345]);" in r, r)
        self.assertTrue('img src="//example.com/piwik.php?idsite=345"'
                        in r, r)

    @override_settings(MATOMO_DOMAIN_PATH='example.com/matomo',
                       MATOMO_SITE_ID='345')
    def test_domain_path_valid(self):
        r = self.render_tag('matomo', 'matomo')
        self.assertTrue('"//example.com/matomo/"' in r, r)

    @override_settings(MATOMO_DOMAIN_PATH='example.com:1234',
                       MATOMO_SITE_ID='345')
    def test_domain_port_valid(self):
        r = self.render_tag('matomo', 'matomo')
        self.assertTrue('"//example.com:1234/";' in r, r)

    @override_settings(MATOMO_DOMAIN_PATH='example.com:1234/matomo',
                       MATOMO_SITE_ID='345')
    def test_domain_port_path_valid(self):
        r = self.render_tag('matomo', 'matomo')
        self.assertTrue('"//example.com:1234/matomo/"' in r, r)

    @override_settings(MATOMO_DOMAIN_PATH=None)
    def test_no_domain(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_SITE_ID=None)
    def test_no_siteid(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_SITE_ID='x')
    def test_siteid_not_a_number(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_DOMAIN_PATH='http://www.example.com')
    def test_domain_protocol_invalid(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_DOMAIN_PATH='example.com/')
    def test_domain_slash_invalid(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_DOMAIN_PATH='example.com:123:456')
    def test_domain_multi_port(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_DOMAIN_PATH='example.com:')
    def test_domain_incomplete_port(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_DOMAIN_PATH='example.com:/matomo')
    def test_domain_uri_incomplete_port(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(MATOMO_DOMAIN_PATH='example.com:12df')
    def test_domain_port_invalid(self):
        self.assertRaises(AnalyticalException, MatomoNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = MatomoNode().render(context)
        self.assertTrue(r.startswith(
            '<!-- Matomo disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

    def test_uservars(self):
        context = Context({'matomo_vars': [(1, 'foo', 'foo_val'),
                                           (2, 'bar', 'bar_val', 'page'),
                                           (3, 'spam', 'spam_val', 'visit')]})
        r = MatomoNode().render(context)
        msg = 'Incorrect Matomo custom variable rendering. Expected:\n%s\nIn:\n%s'
        for var_code in ['_paq.push(["setCustomVariable", 1, "foo", "foo_val", "page"]);',
                         '_paq.push(["setCustomVariable", 2, "bar", "bar_val", "page"]);',
                         '_paq.push(["setCustomVariable", 3, "spam", "spam_val", "visit"]);']:
            self.assertIn(var_code, r, msg % (var_code, r))

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_default_usertrack(self):
        context = Context({
            'user': User(username='BDFL', first_name='Guido', last_name='van Rossum')
        })
        r = MatomoNode().render(context)
        msg = 'Incorrect Matomo user tracking rendering.\nNot found:\n%s\nIn:\n%s'
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        self.assertIn(var_code, r, msg % (var_code, r))

    def test_matomo_usertrack(self):
        context = Context({
            'matomo_identity': 'BDFL'
        })
        r = MatomoNode().render(context)
        msg = 'Incorrect Matomo user tracking rendering.\nNot found:\n%s\nIn:\n%s'
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        self.assertIn(var_code, r, msg % (var_code, r))

    def test_analytical_usertrack(self):
        context = Context({
            'analytical_identity': 'BDFL'
        })
        r = MatomoNode().render(context)
        msg = 'Incorrect Matomo user tracking rendering.\nNot found:\n%s\nIn:\n%s'
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        self.assertIn(var_code, r, msg % (var_code, r))

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_disable_usertrack(self):
        context = Context({
            'user': User(username='BDFL', first_name='Guido', last_name='van Rossum'),
            'matomo_identity': None
        })
        r = MatomoNode().render(context)
        msg = 'Incorrect Matomo user tracking rendering.\nFound:\n%s\nIn:\n%s'
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        self.assertNotIn(var_code, r, msg % (var_code, r))

    @override_settings(MATOMO_DISABLE_COOKIES=True)
    def test_disable_cookies(self):
        r = MatomoNode().render(Context({}))
        self.assertTrue("_paq.push(['disableCookies']);" in r, r)

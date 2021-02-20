"""
Tests for the Piwik template tags and filters.
"""

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.piwik import PiwikNode
from analytical.utils import AnalyticalException


@override_settings(PIWIK_DOMAIN_PATH='example.com', PIWIK_SITE_ID='345')
class PiwikTagTestCase(TagTestCase):
    """
    Tests for the ``piwik`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('piwik', 'piwik')
        assert '"//example.com/"' in r
        assert "_paq.push(['setSiteId', 345]);" in r
        assert 'img src="//example.com/piwik.php?idsite=345"' in r

    def test_node(self):
        r = PiwikNode().render(Context({}))
        assert '"//example.com/";' in r
        assert "_paq.push(['setSiteId', 345]);" in r
        assert 'img src="//example.com/piwik.php?idsite=345"' in r

    @override_settings(PIWIK_DOMAIN_PATH='example.com/piwik',
                       PIWIK_SITE_ID='345')
    def test_domain_path_valid(self):
        r = self.render_tag('piwik', 'piwik')
        assert '"//example.com/piwik/"' in r

    @override_settings(PIWIK_DOMAIN_PATH='example.com:1234',
                       PIWIK_SITE_ID='345')
    def test_domain_port_valid(self):
        r = self.render_tag('piwik', 'piwik')
        assert '"//example.com:1234/";' in r

    @override_settings(PIWIK_DOMAIN_PATH='example.com:1234/piwik',
                       PIWIK_SITE_ID='345')
    def test_domain_port_path_valid(self):
        r = self.render_tag('piwik', 'piwik')
        assert '"//example.com:1234/piwik/"' in r

    @override_settings(PIWIK_DOMAIN_PATH=None)
    def test_no_domain(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_SITE_ID=None)
    def test_no_siteid(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_SITE_ID='x')
    def test_siteid_not_a_number(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_DOMAIN_PATH='http://www.example.com')
    def test_domain_protocol_invalid(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_DOMAIN_PATH='example.com/')
    def test_domain_slash_invalid(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_DOMAIN_PATH='example.com:123:456')
    def test_domain_multi_port(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_DOMAIN_PATH='example.com:')
    def test_domain_incomplete_port(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_DOMAIN_PATH='example.com:/piwik')
    def test_domain_uri_incomplete_port(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(PIWIK_DOMAIN_PATH='example.com:12df')
    def test_domain_port_invalid(self):
        with pytest.raises(AnalyticalException):
            PiwikNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = PiwikNode().render(context)
        assert r.startswith('<!-- Piwik disabled on internal IP address')
        assert r.endswith('-->')

    def test_uservars(self):
        context = Context({'piwik_vars': [(1, 'foo', 'foo_val'),
                                          (2, 'bar', 'bar_val', 'page'),
                                          (3, 'spam', 'spam_val', 'visit')]})
        r = PiwikNode().render(context)
        for var_code in ['_paq.push(["setCustomVariable", 1, "foo", "foo_val", "page"]);',
                         '_paq.push(["setCustomVariable", 2, "bar", "bar_val", "page"]);',
                         '_paq.push(["setCustomVariable", 3, "spam", "spam_val", "visit"]);']:
            assert var_code in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_default_usertrack(self):
        context = Context({
            'user': User(username='BDFL', first_name='Guido', last_name='van Rossum')
        })
        r = PiwikNode().render(context)
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        assert var_code in r

    def test_piwik_usertrack(self):
        context = Context({
            'piwik_identity': 'BDFL'
        })
        r = PiwikNode().render(context)
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        assert var_code in r

    def test_analytical_usertrack(self):
        context = Context({
            'analytical_identity': 'BDFL'
        })
        r = PiwikNode().render(context)
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        assert var_code in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_disable_usertrack(self):
        context = Context({
            'user': User(username='BDFL', first_name='Guido', last_name='van Rossum'),
            'piwik_identity': None
        })
        r = PiwikNode().render(context)
        var_code = '_paq.push(["setUserId", "BDFL"]);'
        assert var_code not in r

    @override_settings(PIWIK_DISABLE_COOKIES=True)
    def test_disable_cookies(self):
        r = PiwikNode().render(Context({}))
        assert "_paq.push(['disableCookies']);" in r

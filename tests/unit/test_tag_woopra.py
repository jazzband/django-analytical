"""
Tests for the Woopra template tags and filters.
"""

from datetime import datetime

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.woopra import WoopraNode
from analytical.utils import AnalyticalException


@override_settings(WOOPRA_DOMAIN='example.com')
class WoopraTagTestCase(TagTestCase):
    """
    Tests for the ``woopra`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('woopra', 'woopra')
        assert 'var woo_settings = {"domain": "example.com"};' in r

    def test_node(self):
        r = WoopraNode().render(Context({}))
        assert 'var woo_settings = {"domain": "example.com"};' in r

    @override_settings(WOOPRA_DOMAIN=None)
    def test_no_domain(self):
        with pytest.raises(AnalyticalException):
            WoopraNode()

    @override_settings(WOOPRA_DOMAIN='this is not a domain')
    def test_wrong_domain(self):
        with pytest.raises(AnalyticalException):
            WoopraNode()

    @override_settings(WOOPRA_IDLE_TIMEOUT=1234)
    def test_idle_timeout(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"domain": "example.com", "idle_timeout": 1234};'
        ) in r

    @override_settings(WOOPRA_COOKIE_NAME='foo')
    def test_cookie_name(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"cookie_name": "foo", "domain": "example.com"};'
        ) in r

    @override_settings(WOOPRA_COOKIE_DOMAIN='.example.com')
    def test_cookie_domain(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"cookie_domain": ".example.com",'
            ' "domain": "example.com"};'
        ) in r

    @override_settings(WOOPRA_COOKIE_PATH='/foo/cookie/path')
    def test_cookie_path(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"cookie_path": "/foo/cookie/path",'
            ' "domain": "example.com"};'
        ) in r

    @override_settings(WOOPRA_COOKIE_EXPIRE='Fri Jan 01 2027 15:00:00 GMT+0000')
    def test_cookie_expire(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"cookie_expire":'
            ' "Fri Jan 01 2027 15:00:00 GMT+0000", "domain": "example.com"};'
        ) in r

    @override_settings(WOOPRA_CLICK_TRACKING=True)
    def test_click_tracking(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"click_tracking": true, "domain": "example.com"};'
        ) in r

    @override_settings(WOOPRA_DOWNLOAD_TRACKING=True)
    def test_download_tracking(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"domain": "example.com", "download_tracking": true};'
        ) in r

    @override_settings(WOOPRA_OUTGOING_TRACKING=True)
    def test_outgoing_tracking(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"domain": "example.com", "outgoing_tracking": true};'
        ) in r

    @override_settings(WOOPRA_OUTGOING_IGNORE_SUBDOMAIN=False)
    def test_outgoing_ignore_subdomain(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"domain": "example.com",'
            ' "outgoing_ignore_subdomain": false};'
        ) in r

    @override_settings(WOOPRA_IGNORE_QUERY_URL=False)
    def test_ignore_query_url(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"domain": "example.com", "ignore_query_url": false};'
        ) in r

    @override_settings(WOOPRA_HIDE_CAMPAIGN=True)
    def test_hide_campaign(self):
        r = WoopraNode().render(Context({}))
        assert (
            'var woo_settings = {"domain": "example.com", "hide_campaign": true};'
        ) in r

    @override_settings(WOOPRA_IDLE_TIMEOUT='1234')
    def test_invalid_int_setting(self):
        with pytest.raises(AnalyticalException, match=r'must be an int'):
            WoopraNode().render(Context({}))

    @override_settings(WOOPRA_HIDE_CAMPAIGN='tomorrow')
    def test_invalid_bool_setting(self):
        with pytest.raises(AnalyticalException, match=r'must be a boolean'):
            WoopraNode().render(Context({}))

    @override_settings(WOOPRA_COOKIE_EXPIRE=datetime.now())
    def test_invalid_str_setting(self):
        with pytest.raises(AnalyticalException, match=r'must be a string'):
            WoopraNode().render(Context({}))

    def test_custom(self):
        r = WoopraNode().render(
            Context(
                {
                    'woopra_var1': 'val1',
                    'woopra_var2': 'val2',
                }
            )
        )
        assert 'var woo_visitor = {"var1": "val1", "var2": "val2"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_name_and_email(self):
        r = WoopraNode().render(
            Context(
                {
                    'user': User(
                        username='test',
                        first_name='Firstname',
                        last_name='Lastname',
                        email='test@example.com',
                    ),
                }
            )
        )
        assert 'var woo_visitor = '
        '{"email": "test@example.com", "name": "Firstname Lastname"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_username_no_email(self):
        r = WoopraNode().render(Context({'user': User(username='test')}))
        assert 'var woo_visitor = {"name": "test"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_no_identify_when_explicit_name(self):
        r = WoopraNode().render(
            Context(
                {
                    'woopra_name': 'explicit',
                    'user': User(username='implicit'),
                }
            )
        )
        assert 'var woo_visitor = {"name": "explicit"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_no_identify_when_explicit_email(self):
        r = WoopraNode().render(
            Context(
                {
                    'woopra_email': 'explicit',
                    'user': User(username='implicit'),
                }
            )
        )
        assert 'var woo_visitor = {"email": "explicit"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = WoopraNode().render(Context({'user': AnonymousUser()}))
        assert 'var woo_visitor = {};' in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = WoopraNode().render(context)
        assert r.startswith('<!-- Woopra disabled on internal IP address')
        assert r.endswith('-->')

"""
Tests for the Woopra template tags and filters.
"""

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
        assert 'var woo_settings = {"domain": "example.com", "idle_timeout": "1234"};' in r

    def test_custom(self):
        r = WoopraNode().render(Context({
            'woopra_var1': 'val1',
            'woopra_var2': 'val2',
        }))
        assert 'var woo_visitor = {"var1": "val1", "var2": "val2"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_name_and_email(self):
        r = WoopraNode().render(Context({
            'user': User(username='test',
                         first_name='Firstname',
                         last_name='Lastname',
                         email="test@example.com"),
        }))
        assert 'var woo_visitor = '
        '{"email": "test@example.com", "name": "Firstname Lastname"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_username_no_email(self):
        r = WoopraNode().render(Context({'user': User(username='test')}))
        assert 'var woo_visitor = {"name": "test"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_no_identify_when_explicit_name(self):
        r = WoopraNode().render(Context({
            'woopra_name': 'explicit',
            'user': User(username='implicit'),
        }))
        assert 'var woo_visitor = {"name": "explicit"};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_no_identify_when_explicit_email(self):
        r = WoopraNode().render(Context({
            'woopra_email': 'explicit',
            'user': User(username='implicit'),
        }))
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

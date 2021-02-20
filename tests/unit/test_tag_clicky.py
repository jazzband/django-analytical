"""
Tests for the Clicky template tags and filters.
"""

import re

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.clicky import ClickyNode
from analytical.utils import AnalyticalException


@override_settings(CLICKY_SITE_ID='12345678')
class ClickyTagTestCase(TagTestCase):
    """
    Tests for the ``clicky`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('clicky', 'clicky')
        assert 'clicky_site_ids.push(12345678);' in r
        assert 'src="//in.getclicky.com/12345678ns.gif"' in r

    def test_node(self):
        r = ClickyNode().render(Context({}))
        assert 'clicky_site_ids.push(12345678);' in r
        assert 'src="//in.getclicky.com/12345678ns.gif"' in r

    @override_settings(CLICKY_SITE_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            ClickyNode()

    @override_settings(CLICKY_SITE_ID='123abc')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            ClickyNode()

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = ClickyNode().render(Context({'user': User(username='test')}))
        assert 'var clicky_custom = {"session": {"username": "test"}};' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = ClickyNode().render(Context({'user': AnonymousUser()}))
        assert 'var clicky_custom = {"session": {"username":' not in r

    def test_custom(self):
        r = ClickyNode().render(Context({
            'clicky_var1': 'val1',
            'clicky_var2': 'val2',
        }))
        assert re.search(r'var clicky_custom = {.*"var1": "val1", "var2": "val2".*};', r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ClickyNode().render(context)
        assert r.startswith('<!-- Clicky disabled on internal IP address')
        assert r.endswith('-->')

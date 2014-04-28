"""
Tests for the Clicky template tags and filters.
"""

import re

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.clicky import ClickyNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(CLICKY_SITE_ID='12345678')
class ClickyTagTestCase(TagTestCase):
    """
    Tests for the ``clicky`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('clicky', 'clicky')
        self.assertTrue('clicky_site_ids.push(12345678);' in r, r)
        self.assertTrue('src="//in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_node(self):
        r = ClickyNode().render(Context({}))
        self.assertTrue('clicky_site_ids.push(12345678);' in r, r)
        self.assertTrue('src="//in.getclicky.com/12345678ns.gif"' in r,
                r)

    @override_settings(CLICKY_SITE_ID=SETTING_DELETED)
    def test_no_site_id(self):
        self.assertRaises(AnalyticalException, ClickyNode)

    @override_settings(CLICKY_SITE_ID='123abc')
    def test_wrong_site_id(self):
        self.assertRaises(AnalyticalException, ClickyNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = ClickyNode().render(Context({'user': User(username='test')}))
        self.assertTrue(
                'var clicky_custom = {"session": {"username": "test"}};' in r,
                r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = ClickyNode().render(Context({'user': AnonymousUser()}))
        self.assertFalse('var clicky_custom = {"session": {"username":' in r, r)

    def test_custom(self):
        r = ClickyNode().render(Context({'clicky_var1': 'val1',
                'clicky_var2': 'val2'}))
        self.assertTrue(re.search('var clicky_custom = {.*'
                '"var1": "val1", "var2": "val2".*};', r), r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ClickyNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Clicky disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

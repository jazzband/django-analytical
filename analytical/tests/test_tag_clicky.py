"""
Tests for the Clicky template tags and filters.
"""

import re

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.clicky import ClickyNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class ClickyTagTestCase(TagTestCase):
    """
    Tests for the ``clicky`` template tag.
    """

    def setUp(self):
        super(ClickyTagTestCase, self).setUp()
        self.settings_manager.set(CLICKY_SITE_ID='12345678')

    def test_tag(self):
        r = self.render_tag('clicky', 'clicky')
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertTrue('src="//in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_node(self):
        r = ClickyNode().render(Context({}))
        self.assertTrue('var clicky_site_id = 12345678;' in r, r)
        self.assertTrue('src="//in.getclicky.com/12345678ns.gif"' in r,
                r)

    def test_no_site_id(self):
        self.settings_manager.delete('CLICKY_SITE_ID')
        self.assertRaises(AnalyticalException, ClickyNode)

    def test_wrong_site_id(self):
        self.settings_manager.set(CLICKY_SITE_ID='123abc')
        self.assertRaises(AnalyticalException, ClickyNode)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = ClickyNode().render(Context({'user': User(username='test')}))
        self.assertTrue(
                'var clicky_custom = {"session": {"username": "test"}};' in r,
                r)

    def test_custom(self):
        r = ClickyNode().render(Context({'clicky_var1': 'val1',
                'clicky_var2': 'val2'}))
        self.assertTrue(re.search('var clicky_custom = {.*'
                '"var1": "val1", "var2": "val2".*};', r), r)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ClickyNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Clicky disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

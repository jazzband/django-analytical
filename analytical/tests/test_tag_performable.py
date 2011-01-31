"""
Tests for the Performable template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.performable import PerformableNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException
from django.contrib.auth.models import User


class PerformableTagTestCase(TagTestCase):
    """
    Tests for the ``performable`` template tag.
    """

    def setUp(self):
        super(PerformableTagTestCase, self).setUp()
        self.settings_manager.set(PERFORMABLE_API_KEY='123ABC')

    def test_tag(self):
        r = self.render_tag('performable', 'performable')
        self.assertTrue('/performable/pax/123ABC.js' in r, r)

    def test_node(self):
        r = PerformableNode().render(Context())
        self.assertTrue('/performable/pax/123ABC.js' in r, r)

    def test_no_api_key(self):
        self.settings_manager.delete('PERFORMABLE_API_KEY')
        self.assertRaises(AnalyticalException, PerformableNode)

    def test_wrong_account_number(self):
        self.settings_manager.set(PERFORMABLE_API_KEY='123AB')
        self.assertRaises(AnalyticalException, PerformableNode)
        self.settings_manager.set(PERFORMABLE_API_KEY='123ABCD')
        self.assertRaises(AnalyticalException, PerformableNode)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = PerformableNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Performable disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = PerformableNode().render(Context({'user': User(username='test')}))
        self.assertTrue('_paq.push(["identify", {identity: "test"}]);' in r, r)


class PerformableEmbedTagTestCase(TagTestCase):
    """
    Tests for the ``performable_embed`` template tag.
    """

    def test_tag(self):
        d = 'example.com'
        p = 'test'
        r = self.render_tag('performable', 'performable_embed "%s" "%s"'
                % (d, p))
        self.assertTrue(
                "$f.initialize({'host': 'example.com', 'page': 'test'});" in r,
                r)

"""
Tests for the Performable template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.performable import PerformableNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException
from django.contrib.auth.models import User


@override_settings(PERFORMABLE_API_KEY='123ABC')
class PerformableTagTestCase(TagTestCase):
    """
    Tests for the ``performable`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('performable', 'performable')
        self.assertTrue('/performable/pax/123ABC.js' in r, r)

    def test_node(self):
        r = PerformableNode().render(Context())
        self.assertTrue('/performable/pax/123ABC.js' in r, r)

    @override_settings(PERFORMABLE_API_KEY=SETTING_DELETED)
    def test_no_api_key(self):
        self.assertRaises(AnalyticalException, PerformableNode)

    @override_settings(PERFORMABLE_API_KEY='123 ABC')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, PerformableNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = PerformableNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Performable disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = PerformableNode().render(Context({'user': User(username='test')}))
        self.assertTrue('_paq.push(["identify", {identity: "test"}]);' in r, r)


class PerformableEmbedTagTestCase(TagTestCase):
    """
    Tests for the ``performable_embed`` template tag.
    """

    def test_tag(self):
        domain = 'example.com'
        page = 'test'
        r = self.render_tag('performable', 'performable_embed "%s" "%s"'
                % (domain, page))
        self.assertTrue(
                "$f.initialize({'host': 'example.com', 'page': 'test'});" in r,
                r)

"""
Tests for the Performable template tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.performable import PerformableNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


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

    @override_settings(PERFORMABLE_API_KEY=None)
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

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = PerformableNode().render(Context({'user': AnonymousUser()}))
        self.assertFalse('_paq.push(["identify", ' in r, r)


class PerformableEmbedTagTestCase(TagTestCase):
    """
    Tests for the ``performable_embed`` template tag.
    """

    def test_tag(self):
        domain = 'example.com'
        page = 'test'
        tag = self.render_tag(
            'performable', 'performable_embed "%s" "%s"' % (domain, page)
        )
        self.assertIn(
            "$f.initialize({'host': 'example.com', 'page': 'test'});", tag
        )

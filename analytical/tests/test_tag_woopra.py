"""
Tests for the Woopra template tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.woopra import WoopraNode
from analytical.tests.utils import TagTestCase, override_settings, \
        SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(WOOPRA_DOMAIN='example.com')
class WoopraTagTestCase(TagTestCase):
    """
    Tests for the ``woopra`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('woopra', 'woopra')
        self.assertTrue('var woo_settings = {"domain": "example.com"};' in r, r)

    def test_node(self):
        r = WoopraNode().render(Context({}))
        self.assertTrue('var woo_settings = {"domain": "example.com"};' in r, r)

    @override_settings(WOOPRA_DOMAIN=SETTING_DELETED)
    def test_no_domain(self):
        self.assertRaises(AnalyticalException, WoopraNode)

    @override_settings(WOOPRA_DOMAIN='this is not a domain')
    def test_wrong_domain(self):
        self.assertRaises(AnalyticalException, WoopraNode)

    @override_settings(WOOPRA_IDLE_TIMEOUT=1234)
    def test_idle_timeout(self):
        r = WoopraNode().render(Context({}))
        self.assertTrue('var woo_settings = {"domain": "example.com", '
                '"idle_timeout": "1234"};' in r, r)

    def test_custom(self):
        r = WoopraNode().render(Context({'woopra_var1': 'val1',
                'woopra_var2': 'val2'}))
        self.assertTrue('var woo_visitor = {"var1": "val1", "var2": "val2"};'
                in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_name_and_email(self):
        r = WoopraNode().render(Context({'user': User(username='test',
                first_name='Firstname', last_name='Lastname',
                email="test@example.com")}))
        self.assertTrue('var woo_visitor = {"name": "Firstname Lastname", '
                '"email": "test@example.com"};' in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_username_no_email(self):
        r = WoopraNode().render(Context({'user': User(username='test')}))
        self.assertTrue('var woo_visitor = {"name": "test"};' in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_no_identify_when_explicit_name(self):
        r = WoopraNode().render(Context({'woopra_name': 'explicit',
                'user': User(username='implicit')}))
        self.assertTrue('var woo_visitor = {"name": "explicit"};' in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_no_identify_when_explicit_email(self):
        r = WoopraNode().render(Context({'woopra_email': 'explicit',
                'user': User(username='implicit')}))
        self.assertTrue('var woo_visitor = {"email": "explicit"};' in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = WoopraNode().render(Context({'user': AnonymousUser()}))
        self.assertTrue('var woo_visitor = {};' in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = WoopraNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Woopra disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

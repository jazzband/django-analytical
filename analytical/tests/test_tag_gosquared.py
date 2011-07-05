"""
Tests for the GoSquared template tags and filters.
"""

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.gosquared import GoSquaredNode
from analytical.tests import override_settings
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(GOSQUARED_SITE_TOKEN='ABC-123456-D')
class GoSquaredTagTestCase(TagTestCase):
    """
    Tests for the ``gosquared`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('gosquared', 'gosquared')
        self.assertTrue('GoSquared.acct = "ABC-123456-D";' in r, r)

    def test_node(self):
        r = GoSquaredNode().render(Context({}))
        self.assertTrue('GoSquared.acct = "ABC-123456-D";' in r, r)

    @override_settings(GOSQUARED_SITE_TOKEN=SETTING_DELETED)
    def test_no_token(self):
        self.assertRaises(AnalyticalException, GoSquaredNode)

    @override_settings(GOSQUARED_SITE_TOKEN='this is not a token')
    def test_wrong_token(self):
        self.assertRaises(AnalyticalException, GoSquaredNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_auto_identify(self):
        r = GoSquaredNode().render(Context({'user': User(username='test',
                first_name='Test', last_name='User')}))
        self.assertTrue('GoSquared.UserName = "Test User";' in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_manual_identify(self):
        r = GoSquaredNode().render(Context({
            'user': User(username='test', first_name='Test', last_name='User'),
            'gosquared_identity': 'test_identity',
        }))
        self.assertTrue('GoSquared.UserName = "test_identity";' in r, r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoSquaredNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- GoSquared disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

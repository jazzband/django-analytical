"""
Tests for the GoSquared template tags and filters.
"""

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.gosquared import GoSquaredNode
from analytical.utils import AnalyticalException


@override_settings(GOSQUARED_SITE_TOKEN='ABC-123456-D')
class GoSquaredTagTestCase(TagTestCase):
    """
    Tests for the ``gosquared`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('gosquared', 'gosquared')
        assert 'GoSquared.acct = "ABC-123456-D";' in r

    def test_node(self):
        r = GoSquaredNode().render(Context({}))
        assert 'GoSquared.acct = "ABC-123456-D";' in r

    @override_settings(GOSQUARED_SITE_TOKEN=None)
    def test_no_token(self):
        with pytest.raises(AnalyticalException):
            GoSquaredNode()

    @override_settings(GOSQUARED_SITE_TOKEN='this is not a token')
    def test_wrong_token(self):
        with pytest.raises(AnalyticalException):
            GoSquaredNode()

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_auto_identify(self):
        r = GoSquaredNode().render(
            Context(
                {
                    'user': User(username='test', first_name='Test', last_name='User'),
                }
            )
        )
        assert 'GoSquared.UserName = "Test User";' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_manual_identify(self):
        r = GoSquaredNode().render(
            Context(
                {
                    'user': User(username='test', first_name='Test', last_name='User'),
                    'gosquared_identity': 'test_identity',
                }
            )
        )
        assert 'GoSquared.UserName = "test_identity";' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = GoSquaredNode().render(Context({'user': AnonymousUser()}))
        assert 'GoSquared.UserName = ' not in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoSquaredNode().render(context)
        assert r.startswith('<!-- GoSquared disabled on internal IP address')
        assert r.endswith('-->')

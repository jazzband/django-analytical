"""
Tests for the Reinvigorate template tags and filters.
"""

import re

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.reinvigorate import ReinvigorateNode
from analytical.tests.utils import TagTestCase, override_settings, \
        SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(REINVIGORATE_TRACKING_ID='12345-abcdefghij')
class ReinvigorateTagTestCase(TagTestCase):
    """
    Tests for the ``reinvigorate`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('reinvigorate', 'reinvigorate')
        self.assertTrue('reinvigorate.track("12345-abcdefghij");' in r, r)

    def test_node(self):
        r = ReinvigorateNode().render(Context({}))
        self.assertTrue('reinvigorate.track("12345-abcdefghij");' in r, r)

    @override_settings(REINVIGORATE_TRACKING_ID=SETTING_DELETED)
    def test_no_tracking_id(self):
        self.assertRaises(AnalyticalException, ReinvigorateNode)

    @override_settings(REINVIGORATE_TRACKING_ID='123abc')
    def test_wrong_tracking_id(self):
        self.assertRaises(AnalyticalException, ReinvigorateNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = ReinvigorateNode().render(Context({'user':
                User(username='test', first_name='Test', last_name='User',
                    email='test@example.com')}))
        self.assertTrue('var re_name_tag = "Test User";' in r, r)
        self.assertTrue('var re_context_tag = "test@example.com";' in r, r)

    def test_tags(self):
        r = ReinvigorateNode().render(Context({'reinvigorate_var1': 'val1',
                'reinvigorate_var2': 2}))
        self.assertTrue(re.search('var re_var1_tag = "val1";', r), r)
        self.assertTrue(re.search('var re_var2_tag = 2;', r), r)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ReinvigorateNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Reinvigorate disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

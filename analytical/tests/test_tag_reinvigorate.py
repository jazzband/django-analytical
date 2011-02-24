"""
Tests for the Reinvigorate template tags and filters.
"""

import re

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.reinvigorate import ReinvigorateNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class ReinvigorateTagTestCase(TagTestCase):
    """
    Tests for the ``reinvigorate`` template tag.
    """

    def setUp(self):
        super(ReinvigorateTagTestCase, self).setUp()
        self.settings_manager.set(REINVIGORATE_TRACKING_ID='12345-abcdefghij')

    def test_tag(self):
        r = self.render_tag('reinvigorate', 'reinvigorate')
        self.assertTrue('reinvigorate.track("12345-abcdefghij");' in r, r)

    def test_node(self):
        r = ReinvigorateNode().render(Context({}))
        self.assertTrue('reinvigorate.track("12345-abcdefghij");' in r, r)

    def test_no_tracking_id(self):
        self.settings_manager.delete('REINVIGORATE_TRACKING_ID')
        self.assertRaises(AnalyticalException, ReinvigorateNode)

    def test_wrong_tracking_id(self):
        self.settings_manager.set(REINVIGORATE_TRACKING_ID='123abc')
        self.assertRaises(AnalyticalException, ReinvigorateNode)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
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

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ReinvigorateNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Reinvigorate disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

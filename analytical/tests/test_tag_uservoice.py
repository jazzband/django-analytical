"""
Tests for the UserVoice tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.uservoice import UserVoiceNode
from analytical.tests.utils import TagTestCase, override_settings, \
        SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(USERVOICE_WIDGET_KEY='abcdefghijklmnopqrst')
class UserVoiceTagTestCase(TagTestCase):
    """
    Tests for the ``uservoice`` template tag.
    """

    def test_node(self):
        r = UserVoiceNode().render(Context())
        self.assertTrue("'widget.uservoice.com/abcdefghijklmnopqrst.js'" in r,
                r)

    def test_tag(self):
        r = self.render_tag('uservoice', 'uservoice')
        self.assertTrue("'widget.uservoice.com/abcdefghijklmnopqrst.js'" in r,
                r)

    @override_settings(USERVOICE_WIDGET_KEY=SETTING_DELETED)
    def test_no_key(self):
        self.assertRaises(AnalyticalException, UserVoiceNode)

    @override_settings(USERVOICE_WIDGET_KEY='abcdefgh ijklmnopqrst')
    def test_invalid_key(self):
        self.assertRaises(AnalyticalException, UserVoiceNode)

    @override_settings(USERVOICE_WIDGET_KEY='')
    def test_empty_key(self):
        r = UserVoiceNode().render(Context())
        self.assertFalse("widget.uservoice.com" in r, r)

    @override_settings(USERVOICE_WIDGET_KEY='')
    def test_overridden_empty_key(self):
        vars = {'uservoice_widget_key': 'bcdefghijklmnopqrstu'}
        r = UserVoiceNode().render(Context(vars))
        self.assertTrue("'widget.uservoice.com/bcdefghijklmnopqrstu.js'" in r,
                r)

    def test_overridden_key(self):
        vars = {'uservoice_widget_key': 'defghijklmnopqrstuvw'}
        r = UserVoiceNode().render(Context(vars))
        self.assertTrue("'widget.uservoice.com/defghijklmnopqrstuvw.js'" in r,
                r)

    def test_link(self):
        r = self.render_tag('uservoice', 'uservoice_popup')
        self.assertEqual(r, "UserVoice.showPopupWidget();")

    def test_link_with_key(self):
        r = self.render_tag('uservoice',
                'uservoice_popup "efghijklmnopqrstuvwx"')
        self.assertEqual(r, 'UserVoice.showPopupWidget({"widget_key": '
                '"efghijklmnopqrstuvwx"});')

    def test_link_disables_tab(self):
        r = self.render_template(
                '{% load uservoice %}{% uservoice_popup %}{% uservoice %}')
        self.assertTrue("UserVoice.showPopupWidget();" in r, r)
        self.assertTrue('"enabled": false' in r, r)
        self.assertTrue("'widget.uservoice.com/abcdefghijklmnopqrst.js'" in r,
                r)

    def test_link_with_key_enables_tab(self):
        r = self.render_template('{% load uservoice %}'
                '{% uservoice_popup "efghijklmnopqrstuvwx" %}{% uservoice %}')
        self.assertTrue('UserVoice.showPopupWidget({"widget_key": '
                '"efghijklmnopqrstuvwx"});' in r, r)
        self.assertTrue('"enabled": true' in r, r)
        self.assertTrue("'widget.uservoice.com/abcdefghijklmnopqrst.js'" in r,
                r)

    def test_custom_fields(self):
        vars = {
            'uservoice_fields': {
                'field1': 'val1',
                'field2': 'val2',
            }
        }
        r = UserVoiceNode().render(Context(vars))
        self.assertTrue('"custom_fields": {"field2": "val2", "field1": "val1"}'
            in r, r)

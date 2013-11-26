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

    @override_settings(USERVOICE_WIDGET_OPTIONS={'key1': 'val1'})
    def test_options(self):
        r = UserVoiceNode().render(Context())
        self.assertTrue("UserVoice.push(['set', {'key1': 'val1'}]);" in r, r)

    @override_settings(USERVOICE_WIDGET_OPTIONS={'key1': 'val1'})
    def test_override_options(self):
        data = {'uservoice_widget_options': {'key1': 'val2'}}
        r = UserVoiceNode().render(Context(data))
        self.assertTrue("UserVoice.push(['set', {'key1': 'val2'}]);" in r, r)

    def test_auto_trigger(self):
        r = UserVoiceNode().render(Context())
        self.assertTrue("UserVoice.push(['addTrigger', {}]);" in r, r)

    @override_settings(USERVOICE_ADD_TRIGGER=False)
    def test_auto_trigger(self):
        r = UserVoiceNode().render(Context())
        self.assertFalse("UserVoice.push(['addTrigger', {}]);" in r, r)

    @override_settings(USERVOICE_ADD_TRIGGER=False)
    def test_auto_trigger_custom_win(self):
        r = UserVoiceNode().render(Context({'uservoice_add_trigger': True}))
        self.assertTrue("UserVoice.push(['addTrigger', {}]);" in r, r)


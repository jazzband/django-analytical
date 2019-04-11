"""
Tests for the UserVoice tags and filters.
"""

from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.uservoice import UserVoiceNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(USERVOICE_WIDGET_KEY='abcdefghijklmnopqrst')
class UserVoiceTagTestCase(TagTestCase):
    """
    Tests for the ``uservoice`` template tag.
    """

    def assertIn(self, element, container):
        try:
            super(TagTestCase, self).assertIn(element, container)
        except AttributeError:
            self.assertTrue(element in container)

    def test_node(self):
        r = UserVoiceNode().render(Context())
        self.assertIn("widget.uservoice.com/abcdefghijklmnopqrst.js", r)

    def test_tag(self):
        r = self.render_tag('uservoice', 'uservoice')
        self.assertIn("widget.uservoice.com/abcdefghijklmnopqrst.js", r)

    @override_settings(USERVOICE_WIDGET_KEY=None)
    def test_no_key(self):
        self.assertRaises(AnalyticalException, UserVoiceNode)

    @override_settings(USERVOICE_WIDGET_KEY='abcdefgh ijklmnopqrst')
    def test_invalid_key(self):
        self.assertRaises(AnalyticalException, UserVoiceNode)

    @override_settings(USERVOICE_WIDGET_KEY='')
    def test_empty_key(self):
        self.assertRaises(AnalyticalException, UserVoiceNode)

    def test_overridden_key(self):
        vars = {'uservoice_widget_key': 'defghijklmnopqrstuvw'}
        r = UserVoiceNode().render(Context(vars))
        self.assertIn("widget.uservoice.com/defghijklmnopqrstuvw.js", r)

    @override_settings(USERVOICE_WIDGET_OPTIONS={'key1': 'val1'})
    def test_options(self):
        r = UserVoiceNode().render(Context())
        self.assertIn("""UserVoice.push(['set', {"key1": "val1"}]);""", r)

    @override_settings(USERVOICE_WIDGET_OPTIONS={'key1': 'val1'})
    def test_override_options(self):
        data = {'uservoice_widget_options': {'key1': 'val2'}}
        r = UserVoiceNode().render(Context(data))
        self.assertIn("""UserVoice.push(['set', {"key1": "val2"}]);""", r)

    def test_auto_trigger_default(self):
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

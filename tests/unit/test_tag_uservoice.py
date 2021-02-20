"""
Tests for the UserVoice tags and filters.
"""

import pytest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.uservoice import UserVoiceNode
from analytical.utils import AnalyticalException


@override_settings(USERVOICE_WIDGET_KEY='abcdefghijklmnopqrst')
class UserVoiceTagTestCase(TagTestCase):
    """
    Tests for the ``uservoice`` template tag.
    """

    def test_node(self):
        r = UserVoiceNode().render(Context())
        assert "widget.uservoice.com/abcdefghijklmnopqrst.js" in r

    def test_tag(self):
        r = self.render_tag('uservoice', 'uservoice')
        assert "widget.uservoice.com/abcdefghijklmnopqrst.js" in r

    @override_settings(USERVOICE_WIDGET_KEY=None)
    def test_no_key(self):
        with pytest.raises(AnalyticalException):
            UserVoiceNode()

    @override_settings(USERVOICE_WIDGET_KEY='abcdefgh ijklmnopqrst')
    def test_invalid_key(self):
        with pytest.raises(AnalyticalException):
            UserVoiceNode()

    @override_settings(USERVOICE_WIDGET_KEY='')
    def test_empty_key(self):
        with pytest.raises(AnalyticalException):
            UserVoiceNode()

    def test_overridden_key(self):
        vars = {'uservoice_widget_key': 'defghijklmnopqrstuvw'}
        r = UserVoiceNode().render(Context(vars))
        assert "widget.uservoice.com/defghijklmnopqrstuvw.js" in r

    @override_settings(USERVOICE_WIDGET_OPTIONS={'key1': 'val1'})
    def test_options(self):
        r = UserVoiceNode().render(Context())
        assert """UserVoice.push(['set', {"key1": "val1"}]);""" in r

    @override_settings(USERVOICE_WIDGET_OPTIONS={'key1': 'val1'})
    def test_override_options(self):
        data = {'uservoice_widget_options': {'key1': 'val2'}}
        r = UserVoiceNode().render(Context(data))
        assert """UserVoice.push(['set', {"key1": "val2"}]);""" in r

    def test_auto_trigger_default(self):
        r = UserVoiceNode().render(Context())
        assert "UserVoice.push(['addTrigger', {}]);" in r

    @override_settings(USERVOICE_ADD_TRIGGER=False)
    def test_auto_trigger(self):
        r = UserVoiceNode().render(Context())
        assert "UserVoice.push(['addTrigger', {}]);" not in r

    @override_settings(USERVOICE_ADD_TRIGGER=False)
    def test_auto_trigger_custom_win(self):
        r = UserVoiceNode().render(Context({'uservoice_add_trigger': True}))
        assert "UserVoice.push(['addTrigger', {}]);" in r

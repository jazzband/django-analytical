"""
Tests for the Olark template tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.template import Context

from analytical.templatetags.olark import OlarkNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(OLARK_SITE_ID='1234-567-89-0123')
class OlarkTestCase(TagTestCase):
    """
    Tests for the ``olark`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('olark', 'olark')
        self.assertTrue("olark.identify('1234-567-89-0123');" in r, r)

    def test_node(self):
        r = OlarkNode().render(Context())
        self.assertTrue("olark.identify('1234-567-89-0123');" in r, r)

    @override_settings(OLARK_SITE_ID=SETTING_DELETED)
    def test_no_site_id(self):
        self.assertRaises(AnalyticalException, OlarkNode)

    @override_settings(OLARK_SITE_ID='1234-567-8901234')
    def test_wrong_site_id(self):
        self.assertRaises(AnalyticalException, OlarkNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = OlarkNode().render(Context({'user':
                User(username='test', first_name='Test', last_name='User')}))
        self.assertTrue("olark('api.chat.updateVisitorNickname', "
                "{snippet: 'Test User (test)'});" in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = OlarkNode().render(Context({'user': AnonymousUser()}))
        self.assertFalse("olark('api.chat.updateVisitorNickname', " in r, r)

    def test_nickname(self):
        r = OlarkNode().render(Context({'olark_nickname': 'testnick'}))
        self.assertTrue("olark('api.chat.updateVisitorNickname', "
                "{snippet: 'testnick'});" in r, r)

    def test_status_string(self):
        r = OlarkNode().render(Context({'olark_status': 'teststatus'}))
        self.assertTrue("olark('api.chat.updateVisitorStatus', "
                '{snippet: "teststatus"});' in r, r)

    def test_status_string_list(self):
        r = OlarkNode().render(Context({'olark_status':
                ['teststatus1', 'teststatus2']}))
        self.assertTrue("olark('api.chat.updateVisitorStatus', "
                '{snippet: ["teststatus1", "teststatus2"]});' in r, r)

    def test_messages(self):
        messages = [
            "welcome_title",
            "chatting_title",
            "unavailable_title",
            "busy_title",
            "away_message",
            "loading_title",
            "welcome_message",
            "busy_message",
            "chat_input_text",
            "name_input_text",
            "email_input_text",
            "offline_note_message",
            "send_button_text",
            "offline_note_thankyou_text",
            "offline_note_error_text",
            "offline_note_sending_text",
            "operator_is_typing_text",
            "operator_has_stopped_typing_text",
            "introduction_error_text",
            "introduction_messages",
            "introduction_submit_button_text",
        ]
        vars = dict(('olark_%s' % m, m) for m in messages)
        r = OlarkNode().render(Context(vars))
        for m in messages:
            self.assertTrue("olark.configure('locale.%s', \"%s\");" % (m, m)
                    in r, r)

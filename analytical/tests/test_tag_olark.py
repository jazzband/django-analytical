"""
Tests for the Olark template tags and filters.
"""

from django.contrib.auth.models import User
from django.template import Context

from analytical.templatetags.olark import OlarkNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class OlarkTestCase(TagTestCase):
    """
    Tests for the ``olark`` template tag.
    """

    def setUp(self):
        super(OlarkTestCase, self).setUp()
        self.settings_manager.set(OLARK_SITE_ID='1234-567-89-0123')

    def test_tag(self):
        r = self.render_tag('olark', 'olark')
        self.assertTrue("olark.identify('1234-567-89-0123');" in r, r)

    def test_node(self):
        r = OlarkNode().render(Context())
        self.assertTrue("olark.identify('1234-567-89-0123');" in r, r)

    def test_no_site_id(self):
        self.settings_manager.delete('OLARK_SITE_ID')
        self.assertRaises(AnalyticalException, OlarkNode)

    def test_wrong_site_id(self):
        self.settings_manager.set(OLARK_SITE_ID='1234-567-8901234')
        self.assertRaises(AnalyticalException, OlarkNode)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = OlarkNode().render(Context({'user':
                User(username='test', first_name='Test', last_name='User')}))
        self.assertTrue("olark('api.chat.updateVisitorNickname', "
                "{snippet: 'Test User (test)'});" in r, r)

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

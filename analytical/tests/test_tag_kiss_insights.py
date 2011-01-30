"""
Tests for the KISSinsights template tags and filters.
"""

from django.contrib.auth.models import User
from django.template import Context

from analytical.templatetags.kiss_insights import KissInsightsNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class KissInsightsTagTestCase(TagTestCase):
    """
    Tests for the ``kiss_insights`` template tag.
    """

    def setUp(self):
        super(KissInsightsTagTestCase, self).setUp()
        self.settings_manager.set(KISS_INSIGHTS_ACCOUNT_NUMBER='12345')
        self.settings_manager.set(KISS_INSIGHTS_SITE_CODE='abc')

    def test_tag(self):
        r = self.render_tag('kiss_insights', 'kiss_insights')
        self.assertTrue("//s3.amazonaws.com/ki.js/12345/abc.js" in r, r)

    def test_node(self):
        r = KissInsightsNode().render(Context())
        self.assertTrue("//s3.amazonaws.com/ki.js/12345/abc.js" in r, r)

    def test_no_account_number(self):
        self.settings_manager.delete('KISS_INSIGHTS_ACCOUNT_NUMBER')
        self.assertRaises(AnalyticalException, KissInsightsNode)

    def test_no_site_code(self):
        self.settings_manager.delete('KISS_INSIGHTS_SITE_CODE')
        self.assertRaises(AnalyticalException, KissInsightsNode)

    def test_wrong_account_number(self):
        self.settings_manager.set(KISS_INSIGHTS_ACCOUNT_NUMBER='abcde')
        self.assertRaises(AnalyticalException, KissInsightsNode)

    def test_wrong_site_id(self):
        self.settings_manager.set(KISS_INSIGHTS_SITE_CODE='ab')
        self.assertRaises(AnalyticalException, KissInsightsNode)
        self.settings_manager.set(KISS_INSIGHTS_SITE_CODE='abcd')
        self.assertRaises(AnalyticalException, KissInsightsNode)

    def test_identify(self):
        self.settings_manager.set(ANALYTICAL_AUTO_IDENTIFY=True)
        r = KissInsightsNode().render(Context({'user': User(username='test')}))
        self.assertTrue("_kiq.push(['identify', 'test']);" in r, r)

    def test_show_survey(self):
        r = KissInsightsNode().render(
                Context({'kiss_insights_show_survey': 1234}))
        self.assertTrue("_kiq.push(['showSurvey', 1234]);" in r, r)

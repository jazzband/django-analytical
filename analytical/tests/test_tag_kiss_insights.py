"""
Tests for the KISSinsights template tags and filters.
"""

from django.contrib.auth.models import User
from django.template import Context

from analytical.templatetags.kiss_insights import KissInsightsNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(KISS_INSIGHTS_ACCOUNT_NUMBER='12345',
        KISS_INSIGHTS_SITE_CODE='abc')
class KissInsightsTagTestCase(TagTestCase):
    """
    Tests for the ``kiss_insights`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('kiss_insights', 'kiss_insights')
        self.assertTrue("//s3.amazonaws.com/ki.js/12345/abc.js" in r, r)

    def test_node(self):
        r = KissInsightsNode().render(Context())
        self.assertTrue("//s3.amazonaws.com/ki.js/12345/abc.js" in r, r)

    @override_settings(KISS_INSIGHTS_ACCOUNT_NUMBER=SETTING_DELETED)
    def test_no_account_number(self):
        self.assertRaises(AnalyticalException, KissInsightsNode)

    @override_settings(KISS_INSIGHTS_SITE_CODE=SETTING_DELETED)
    def test_no_site_code(self):
        self.assertRaises(AnalyticalException, KissInsightsNode)

    @override_settings(KISS_INSIGHTS_ACCOUNT_NUMBER='abcde')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, KissInsightsNode)

    @override_settings(KISS_INSIGHTS_SITE_CODE='abc def')
    def test_wrong_site_id(self):
        self.assertRaises(AnalyticalException, KissInsightsNode)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = KissInsightsNode().render(Context({'user': User(username='test')}))
        self.assertTrue("_kiq.push(['identify', 'test']);" in r, r)

    def test_show_survey(self):
        r = KissInsightsNode().render(
                Context({'kiss_insights_show_survey': 1234}))
        self.assertTrue("_kiq.push(['showSurvey', 1234]);" in r, r)

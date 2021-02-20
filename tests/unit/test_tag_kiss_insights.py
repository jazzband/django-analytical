"""
Tests for the KISSinsights template tags and filters.
"""

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.kiss_insights import KissInsightsNode
from analytical.utils import AnalyticalException


@override_settings(KISS_INSIGHTS_ACCOUNT_NUMBER='12345', KISS_INSIGHTS_SITE_CODE='abc')
class KissInsightsTagTestCase(TagTestCase):
    """
    Tests for the ``kiss_insights`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('kiss_insights', 'kiss_insights')
        assert "//s3.amazonaws.com/ki.js/12345/abc.js" in r

    def test_node(self):
        r = KissInsightsNode().render(Context())
        assert "//s3.amazonaws.com/ki.js/12345/abc.js" in r

    @override_settings(KISS_INSIGHTS_ACCOUNT_NUMBER=None)
    def test_no_account_number(self):
        with pytest.raises(AnalyticalException):
            KissInsightsNode()

    @override_settings(KISS_INSIGHTS_SITE_CODE=None)
    def test_no_site_code(self):
        with pytest.raises(AnalyticalException):
            KissInsightsNode()

    @override_settings(KISS_INSIGHTS_ACCOUNT_NUMBER='abcde')
    def test_wrong_account_number(self):
        with pytest.raises(AnalyticalException):
            KissInsightsNode()

    @override_settings(KISS_INSIGHTS_SITE_CODE='abc def')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            KissInsightsNode()

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = KissInsightsNode().render(Context({'user': User(username='test')}))
        assert "_kiq.push(['identify', 'test']);" in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = KissInsightsNode().render(Context({'user': AnonymousUser()}))
        assert "_kiq.push(['identify', " not in r

    def test_show_survey(self):
        r = KissInsightsNode().render(Context({'kiss_insights_show_survey': 1234}))
        assert "_kiq.push(['showSurvey', 1234]);" in r

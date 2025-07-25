"""
Tests for the Rating@Mail.ru template tags and filters.
"""

import pytest
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.rating_mailru import RatingMailruNode
from analytical.utils import AnalyticalException


@override_settings(RATING_MAILRU_COUNTER_ID='1234567')
class RatingMailruTagTestCase(TagTestCase):
    """
    Tests for the ``rating_mailru`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('rating_mailru', 'rating_mailru')
        assert 'counter?id=1234567;js=na' in r

    def test_node(self):
        r = RatingMailruNode().render(Context({}))
        assert 'counter?id=1234567;js=na' in r

    @override_settings(RATING_MAILRU_COUNTER_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            RatingMailruNode()

    @override_settings(RATING_MAILRU_COUNTER_ID='1234abc')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            RatingMailruNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = RatingMailruNode().render(context)
        assert r.startswith('<!-- Rating@Mail.ru disabled on internal IP address')
        assert r.endswith('-->')

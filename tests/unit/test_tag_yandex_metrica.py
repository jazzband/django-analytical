"""
Tests for the Yandex.Metrica template tags and filters.
"""


from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.yandex_metrica import YandexMetricaNode
from utils import TagTestCase
from analytical.utils import AnalyticalException

import pytest


@override_settings(YANDEX_METRICA_COUNTER_ID='12345678')
class YandexMetricaTagTestCase(TagTestCase):
    """
    Tests for the ``yandex_metrica`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('yandex_metrica', 'yandex_metrica')
        assert "w.yaCounter12345678 = new Ya.Metrika" in r

    def test_node(self):
        r = YandexMetricaNode().render(Context({}))
        assert "w.yaCounter12345678 = new Ya.Metrika" in r

    @override_settings(YANDEX_METRICA_COUNTER_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            YandexMetricaNode()

    @override_settings(YANDEX_METRICA_COUNTER_ID='1234abcd')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            YandexMetricaNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = YandexMetricaNode().render(context)
        assert r.startswith('<!-- Yandex.Metrica disabled on internal IP address')
        assert r.endswith('-->')

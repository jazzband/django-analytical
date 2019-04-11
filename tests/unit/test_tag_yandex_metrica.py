"""
Tests for the Yandex.Metrica template tags and filters.
"""


from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.yandex_metrica import YandexMetricaNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(YANDEX_METRICA_COUNTER_ID='12345678')
class YandexMetricaTagTestCase(TagTestCase):
    """
    Tests for the ``yandex_metrica`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('yandex_metrica', 'yandex_metrica')
        self.assertTrue("w.yaCounter12345678 = new Ya.Metrika" in r, r)

    def test_node(self):
        r = YandexMetricaNode().render(Context({}))
        self.assertTrue("w.yaCounter12345678 = new Ya.Metrika" in r, r)

    @override_settings(YANDEX_METRICA_COUNTER_ID=None)
    def test_no_site_id(self):
        self.assertRaises(AnalyticalException, YandexMetricaNode)

    @override_settings(YANDEX_METRICA_COUNTER_ID='1234abcd')
    def test_wrong_site_id(self):
        self.assertRaises(AnalyticalException, YandexMetricaNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = YandexMetricaNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Yandex.Metrica disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

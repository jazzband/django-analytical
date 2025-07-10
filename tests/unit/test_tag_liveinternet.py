"""
Tests for the LiveInternet template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.liveinternet import (LiveInternetNode,
                                                  LIVEINTERNET_WITH_IMAGE,
                                                  LIVEINTERNET_CODE,
                                                  LIVEINTERNET_IMAGE)
from utils import TagTestCase


class LiveInternetTagTestCase(TagTestCase):
    """
    Tests for the ``liveinternet`` template tag.
    """

    def test_render_liveinternet(self):
        response = self.render_tag('liveinternet', 'liveinternet')
        assert '<a href="https://www.liveinternet.ru/click"' in response

    def test_render_liveinternet_code(self):
        response = self.render_tag('liveinternet', 'liveinternet_code')
        assert 'new Image().src = "https://counter.yadro.ru/hit?r"' in response

    def test_render_liveinternet_img(self):
        response = self.render_tag('liveinternet', 'liveinternet_img')
        assert '<a href="https://www.liveinternet.ru/click"' in response

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_liveinternet_render_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = LiveInternetNode(LIVEINTERNET_WITH_IMAGE, 'liveinternet_with_image').render(context)
        assert r.startswith('<!-- liveinternet disabled on internal IP address')
        assert r.endswith('-->')

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_liveinternet_code_render_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = LiveInternetNode(LIVEINTERNET_CODE, 'liveinternet_code').render(context)
        assert r.startswith('<!-- liveinternet_code disabled on internal IP address')
        assert r.endswith('-->')

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_liveinternet_img_render_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = LiveInternetNode(LIVEINTERNET_IMAGE, 'liveinternet_image').render(context)
        assert r.startswith('<!-- liveinternet_img disabled on internal IP address')
        assert r.endswith('-->')

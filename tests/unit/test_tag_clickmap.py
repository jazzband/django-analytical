"""
Tests for the Clickmap template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.clickmap import ClickmapNode
from utils import TagTestCase
from analytical.utils import AnalyticalException

import pytest


@override_settings(CLICKMAP_TRACKER_ID='12345ABC')
class ClickmapTagTestCase(TagTestCase):
    """
    Tests for the ``clickmap`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('clickmap', 'clickmap')
        assert "tracker: '12345ABC', version:'2'};" in r

    def test_node(self):
        r = ClickmapNode().render(Context({}))
        assert "tracker: '12345ABC', version:'2'};" in r

    @override_settings(CLICKMAP_TRACKER_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            ClickmapNode()

    @override_settings(CLICKMAP_TRACKER_ID='ab#c')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            ClickmapNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ClickmapNode().render(context)
        assert r.startswith('<!-- Clickmap disabled on internal IP address')
        assert r.endswith('-->')

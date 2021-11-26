"""
Tests for the Heap template tags and filters.
"""

import pytest
from django.http import HttpRequest
from django.template import Context, Template, TemplateSyntaxError
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.heap import HeapNode
from analytical.utils import AnalyticalException


@override_settings(HEAP_TRACKER_ID='123456789')
class HeapTagTestCase(TagTestCase):
    """
    Tests for the ``heap`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('heap', 'heap')
        assert "123456789" in r

    def test_node(self):
        r = HeapNode().render(Context({}))
        assert "123456789" in r

    def test_tags_take_no_args(self):
        with pytest.raises(TemplateSyntaxError, match="'heap' takes no arguments"):
            Template('{% load heap %}{% heap "arg" %}').render(Context({}))

    @override_settings(HEAP_TRACKER_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            HeapNode()

    @override_settings(HEAP_TRACKER_ID='abcdefg')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            HeapNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = HeapNode().render(context)
        assert r.startswith('<!-- Heap disabled on internal IP address')
        assert r.endswith('-->')

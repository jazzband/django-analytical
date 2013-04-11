"""
Tests for the Clickmap template tags and filters.
"""

import re

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.clickmap import ClickmapNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(CLICKMAP_TRACKER_ID='12345')
class ClickyTagTestCase(TagTestCase):
    """
    Tests for the ``clickmap`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('clicjmap', 'clickmap')
        self.assertTrue("tracker: '12345', version:'2'};" in r, r)

    def test_node(self):
        r = ClickmapNode().render(Context({}))
        self.assertTrue("tracker: '12345', version:'2'};" in r, r)

    @override_settings(CLICKMAP_TRACKER_ID=SETTING_DELETED)
    def test_no_site_id(self):
        self.assertRaises(AnalyticalException, ClickmapNode)

    @override_settings(CLICKMAP_TRACKER_ID='abc')
    def test_wrong_site_id(self):
        self.assertRaises(AnalyticalException, ClickyNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = ClickmapNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Clickmap disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

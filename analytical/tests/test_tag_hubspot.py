"""
Tests for the HubSpot template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.hubspot import HubSpotNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(HUBSPOT_PORTAL_ID='1234')
class HubSpotTagTestCase(TagTestCase):
    """
    Tests for the ``hubspot`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('hubspot', 'hubspot')
        self.assertTrue("n.id=i;n.src='//js.hs-analytics.net/analytics/'"
                        "+(Math.ceil(new Date()/r)*r)+'/1234.js';" in r, r)

    def test_node(self):
        r = HubSpotNode().render(Context())
        self.assertTrue("n.id=i;n.src='//js.hs-analytics.net/analytics/'"
                        "+(Math.ceil(new Date()/r)*r)+'/1234.js';" in r, r)

    @override_settings(HUBSPOT_PORTAL_ID=None)
    def test_no_portal_id(self):
        self.assertRaises(AnalyticalException, HubSpotNode)

    @override_settings(HUBSPOT_PORTAL_ID='wrong')
    def test_wrong_portal_id(self):
        self.assertRaises(AnalyticalException, HubSpotNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = HubSpotNode().render(context)
        self.assertTrue(r.startswith('<!-- HubSpot disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

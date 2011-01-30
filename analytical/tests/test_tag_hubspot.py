"""
Tests for the HubSpot template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.hubspot import HubSpotNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


class HubSpotTagTestCase(TagTestCase):
    """
    Tests for the ``hubspot`` template tag.
    """

    def setUp(self):
        super(HubSpotTagTestCase, self).setUp()
        self.settings_manager.set(HUBSPOT_PORTAL_ID='1234')
        self.settings_manager.set(HUBSPOT_DOMAIN='example.com')

    def test_tag(self):
        r = self.render_tag('hubspot', 'hubspot')
        self.assertTrue('var hs_portalid = 1234;' in r, r)
        self.assertTrue('var hs_ppa = "example.com";' in r, r)

    def test_node(self):
        r = HubSpotNode().render(Context())
        self.assertTrue('var hs_portalid = 1234;' in r, r)
        self.assertTrue('var hs_ppa = "example.com";' in r, r)

    def test_no_portal_id(self):
        self.settings_manager.delete('HUBSPOT_PORTAL_ID')
        self.assertRaises(AnalyticalException, HubSpotNode)

    def test_wrong_portal_id(self):
        self.settings_manager.set(HUBSPOT_PORTAL_ID='wrong')
        self.assertRaises(AnalyticalException, HubSpotNode)

    def test_no_domain(self):
        self.settings_manager.delete('HUBSPOT_DOMAIN')
        self.assertRaises(AnalyticalException, HubSpotNode)

    def test_wrong_domain(self):
        self.settings_manager.set(HUBSPOT_DOMAIN='wrong domain')
        self.assertRaises(AnalyticalException, HubSpotNode)

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = HubSpotNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- HubSpot disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

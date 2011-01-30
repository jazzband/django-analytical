"""
Tests for the generic template tags and filters.
"""

from django.template import Context, Template

from analytical.templatetags import analytical
from analytical.tests.utils import TagTestCase


class AnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``analytical`` template tags.
    """

    def setUp(self):
        super(AnalyticsTagTestCase, self).setUp()
        self._tag_modules = analytical.TAG_MODULES
        analytical.TAG_MODULES = ['analytical.tests.dummy']
        analytical.template_nodes = analytical._load_template_nodes()

    def tearDown(self):
        analytical.TAG_MODULES = self._tag_modules
        analytical.template_nodes = analytical._load_template_nodes()
        super(AnalyticsTagTestCase, self).tearDown()

    def render_location_tag(self, location, vars=None):
        if vars is None:
            vars = {}
        t = Template("{%% load analytical %%}{%% analytical_%s %%}"
                % location)
        return t.render(Context(vars))

    def test_location_tags(self):
        for l in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(l)
            self.assertTrue('dummy_%s' % l in r, r)

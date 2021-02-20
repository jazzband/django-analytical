"""
Tests for the generic template tags and filters.
"""

from django.template import Context, Template
from utils import TagTestCase

from analytical.templatetags import analytical


class AnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``analytical`` template tags.
    """

    def setUp(self):
        super().setUp()
        self._tag_modules = analytical.TAG_MODULES
        analytical.TAG_MODULES = ['tests.testproject.dummy']
        analytical.template_nodes = analytical._load_template_nodes()

    def tearDown(self):
        analytical.TAG_MODULES = self._tag_modules
        analytical.template_nodes = analytical._load_template_nodes()
        super().tearDown()

    def render_location_tag(self, location, vars=None):
        if vars is None:
            vars = {}
        t = Template("{%% load analytical %%}{%% analytical_%s %%}" % location)
        return t.render(Context(vars))

    def test_location_tags(self):
        for loc in ['head_top', 'head_bottom', 'body_top', 'body_bottom']:
            r = self.render_location_tag(loc)
            assert f'dummy_{loc}' in r

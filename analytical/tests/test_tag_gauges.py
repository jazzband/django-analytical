"""
Tests for the Gauges template tags and filters.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.gauges import GaugesNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(GAUGES_SITE_ID='1234567890abcdef0123456789')
class GaugesTagTestCase(TagTestCase):
    """
    Tests for the ``gauges`` template tag.
    """

    def test_tag(self):
        self.assertEqual("""
    <script type="text/javascript">
      var _gauges = _gauges || [];
      (function() {
        var t   = document.createElement('script');
        t.type  = 'text/javascript';
        t.async = true;
        t.id    = 'gauges-tracker';
        t.setAttribute('data-site-id', '1234567890abcdef0123456789');
        t.src = '//secure.gaug.es/track.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(t, s);
      })();
    </script>
""",
                self.render_tag('gauges', 'gauges'))

    def test_node(self):
        self.assertEqual(
                """
    <script type="text/javascript">
      var _gauges = _gauges || [];
      (function() {
        var t   = document.createElement('script');
        t.type  = 'text/javascript';
        t.async = true;
        t.id    = 'gauges-tracker';
        t.setAttribute('data-site-id', '1234567890abcdef0123456789');
        t.src = '//secure.gaug.es/track.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(t, s);
      })();
    </script>
""",
                GaugesNode().render(Context()))

    @override_settings(GAUGES_SITE_ID=SETTING_DELETED)
    def test_no_account_number(self):
        self.assertRaises(AnalyticalException, GaugesNode)

    @override_settings(GAUGES_SITE_ID='123abQ')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, GaugesNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GaugesNode().render(context)
        self.assertTrue(r.startswith(
                '<!-- Gauges disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

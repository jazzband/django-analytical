"""
Tests for the Gauges template tags and filters.
"""

import pytest
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.gauges import GaugesNode
from analytical.utils import AnalyticalException


@override_settings(GAUGES_SITE_ID='1234567890abcdef0123456789')
class GaugesTagTestCase(TagTestCase):
    """
    Tests for the ``gauges`` template tag.
    """

    def test_tag(self):
        assert (
            self.render_tag('gauges', 'gauges')
            == """
    <script>
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
"""
        )

    def test_node(self):
        assert (
            GaugesNode().render(Context())
            == """
    <script>
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
"""
        )

    @override_settings(GAUGES_SITE_ID=None)
    def test_no_account_number(self):
        with pytest.raises(AnalyticalException):
            GaugesNode()

    @override_settings(GAUGES_SITE_ID='123abQ')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, GaugesNode)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GaugesNode().render(context)
        assert r.startswith('<!-- Gauges disabled on internal IP address')
        assert r.endswith('-->')

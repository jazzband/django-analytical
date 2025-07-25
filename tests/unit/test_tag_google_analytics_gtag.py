"""
Tests for the Google Analytics template tags and filters, using the new gtag.js library.
"""

import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.google_analytics_gtag import GoogleAnalyticsGTagNode
from analytical.utils import AnalyticalException


@override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='UA-123456-7')
class GoogleAnalyticsTagTestCase(TagTestCase):
    """
    Tests for the ``google_analytics_gtag`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('google_analytics_gtag', 'google_analytics_gtag')
        assert (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123456-7"></script>'
        ) in r
        assert "gtag('js', new Date());" in r
        assert "gtag('config', 'UA-123456-7', {});" in r

    def test_node(self):
        r = GoogleAnalyticsGTagNode().render(Context())
        assert (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-123456-7"></script>'
        ) in r
        assert "gtag('js', new Date());" in r
        assert "gtag('config', 'UA-123456-7', {});" in r

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID=None)
    def test_no_property_id(self):
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsGTagNode()

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='wrong')
    def test_wrong_property_id(self):
        with pytest.raises(AnalyticalException):
            GoogleAnalyticsGTagNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = GoogleAnalyticsGTagNode().render(context)
        assert r.startswith('<!-- Google Analytics disabled on internal IP address')
        assert r.endswith('-->')

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = GoogleAnalyticsGTagNode().render(Context({'user': User(username='test')}))
        assert 'gtag(\'config\', \'UA-123456-7\', {"user_id": "test"});' in r

    def test_identity_context_specific_provider(self):
        """
        The user_id variable must be set according to
        google_analytics_gtag_identity variable in the context.
        """
        r = GoogleAnalyticsGTagNode().render(
            Context(
                {
                    'google_analytics_gtag_identity': 'foo_gtag_identity',
                    'user': User(username='test'),
                }
            )
        )
        assert (
            'gtag(\'config\', \'UA-123456-7\', {"user_id": "foo_gtag_identity"});' in r
        )

    def test_identity_context_general(self):
        """
        The user_id variable must be set according to analytical_identity variable in the context.
        """
        r = GoogleAnalyticsGTagNode().render(
            Context(
                {
                    'analytical_identity': 'bar_analytical_identity',
                    'user': User(username='test'),
                }
            )
        )
        assert (
            'gtag(\'config\', \'UA-123456-7\', {"user_id": "bar_analytical_identity"});'
            in r
        )

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='G-12345678')
    def test_tag_with_measurement_id(self):
        r = self.render_tag('google_analytics_gtag', 'google_analytics_gtag')
        assert (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-12345678"></script>'
        ) in r
        assert "gtag('js', new Date());" in r
        assert "gtag('config', 'G-12345678', {});" in r

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='AW-1234567890')
    def test_tag_with_conversion_id(self):
        r = self.render_tag('google_analytics_gtag', 'google_analytics_gtag')
        assert (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=AW-1234567890"></script'
        ) in r
        assert "gtag('js', new Date());" in r
        assert "gtag('config', 'AW-1234567890', {});" in r

    @override_settings(GOOGLE_ANALYTICS_GTAG_PROPERTY_ID='DC-12345678')
    def test_tag_with_advertiser_id(self):
        r = self.render_tag('google_analytics_gtag', 'google_analytics_gtag')
        assert (
            '<script async src="https://www.googletagmanager.com/gtag/js?id=DC-12345678"></script>'
        ) in r
        assert "gtag('js', new Date());" in r
        assert "gtag('config', 'DC-12345678', {});" in r

    def test_tag_with_custom_dimensions(self):
        r = GoogleAnalyticsGTagNode().render(
            Context(
                {
                    'google_analytics_custom_dimensions': {
                        'dimension_1': 'foo',
                        'dimension_2': 'bar',
                        'user_properties': {
                            'user_property_1': True,
                            'user_property_2': 'xyz',
                        },
                    },
                }
            )
        )
        assert (
            "gtag('config', 'UA-123456-7', {"
            '"dimension_1": "foo", '
            '"dimension_2": "bar", '
            '"user_properties": {'
            '"user_property_1": true, '
            '"user_property_2": "xyz"}});' in r
        )

    def test_tag_with_identity_and_custom_dimensions(self):
        r = GoogleAnalyticsGTagNode().render(
            Context(
                {
                    'google_analytics_gtag_identity': 'foo_gtag_identity',
                    'google_analytics_custom_dimensions': {
                        'dimension_1': 'foo',
                        'dimension_2': 'bar',
                    },
                }
            )
        )
        assert (
            "gtag('config', 'UA-123456-7', {"
            '"dimension_1": "foo", '
            '"dimension_2": "bar", '
            '"user_id": "foo_gtag_identity"});' in r
        )

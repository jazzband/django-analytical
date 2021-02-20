"""
Tests for the SnapEngage template tags and filters.
"""

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.template import Context
from django.test.utils import override_settings
from django.utils import translation
from utils import TagTestCase

from analytical.templatetags.snapengage import (
    BUTTON_LOCATION_BOTTOM,
    BUTTON_LOCATION_LEFT,
    BUTTON_LOCATION_RIGHT,
    BUTTON_LOCATION_TOP,
    BUTTON_STYLE_DEFAULT,
    BUTTON_STYLE_LIVE,
    BUTTON_STYLE_NONE,
    FORM_POSITION_TOP_LEFT,
    SnapEngageNode,
)
from analytical.utils import AnalyticalException

WIDGET_ID = 'ec329c69-0bf0-4db8-9b77-3f8150fb977e'


@override_settings(
    SNAPENGAGE_WIDGET_ID=WIDGET_ID,
    SNAPENGAGE_BUTTON=BUTTON_STYLE_DEFAULT,
    SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_LEFT,
    SNAPENGAGE_BUTTON_OFFSET="55%",
)
class SnapEngageTestCase(TagTestCase):
    """
    Tests for the ``snapengage`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('snapengage', 'snapengage')
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","55%");' in r

    def test_node(self):
        r = SnapEngageNode().render(Context())
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","55%");' in r

    @override_settings(SNAPENGAGE_WIDGET_ID=None)
    def test_no_site_id(self):
        with pytest.raises(AnalyticalException):
            SnapEngageNode()

    @override_settings(SNAPENGAGE_WIDGET_ID='abc')
    def test_wrong_site_id(self):
        with pytest.raises(AnalyticalException):
            SnapEngageNode()

    def test_no_button(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button': BUTTON_STYLE_NONE,
        }))
        assert 'SnapABug.init("ec329c69-0bf0-4db8-9b77-3f8150fb977e")' in r
        with override_settings(SNAPENGAGE_BUTTON=BUTTON_STYLE_NONE):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.init("ec329c69-0bf0-4db8-9b77-3f8150fb977e")' in r

    def test_live_button(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button': BUTTON_STYLE_LIVE,
        }))
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","55%",true);' in r
        with override_settings(SNAPENGAGE_BUTTON=BUTTON_STYLE_LIVE):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","55%",true);' in r

    def test_custom_button(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button': "http://www.example.com/button.png",
        }))
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","55%");' in r
        assert 'SnapABug.setButton("http://www.example.com/button.png");' in r
        with override_settings(
                SNAPENGAGE_BUTTON="http://www.example.com/button.png"):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","55%");' in r
            assert 'SnapABug.setButton("http://www.example.com/button.png");' in r

    def test_button_location_right(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location': BUTTON_LOCATION_RIGHT,
        }))
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","1","55%");' in r
        with override_settings(SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_RIGHT):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","1","55%");' in r

    def test_button_location_top(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location': BUTTON_LOCATION_TOP,
        }))
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","2","55%");' in r
        with override_settings(SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_TOP):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","2","55%");' in r

    def test_button_location_bottom(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location': BUTTON_LOCATION_BOTTOM,
        }))
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","3","55%");' in r
        with override_settings(
                SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_BOTTOM):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","3","55%");' in r

    def test_button_offset(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location_offset': "30%",
        }))
        assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","30%");' in r
        with override_settings(SNAPENGAGE_BUTTON_LOCATION_OFFSET="30%"):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0","30%");' in r

    def test_button_effect(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_effect': "-4px",
        }))
        assert 'SnapABug.setButtonEffect("-4px");' in r
        with override_settings(SNAPENGAGE_BUTTON_EFFECT="-4px"):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setButtonEffect("-4px");' in r

    def test_form_position(self):
        r = SnapEngageNode().render(Context({
            'snapengage_form_position': FORM_POSITION_TOP_LEFT,
        }))
        assert 'SnapABug.setChatFormPosition("tl");' in r
        with override_settings(SNAPENGAGE_FORM_POSITION=FORM_POSITION_TOP_LEFT):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setChatFormPosition("tl");' in r

    def test_form_top_position(self):
        r = SnapEngageNode().render(Context({
            'snapengage_form_top_position': 40,
        }))
        assert 'SnapABug.setFormTopPosition(40);' in r
        with override_settings(SNAPENGAGE_FORM_TOP_POSITION=40):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setFormTopPosition(40);' in r

    def test_domain(self):
        r = SnapEngageNode().render(Context({
            'snapengage_domain': "example.com"}))
        assert 'SnapABug.setDomain("example.com");' in r
        with override_settings(SNAPENGAGE_DOMAIN="example.com"):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setDomain("example.com");' in r

    def test_secure_connection(self):
        r = SnapEngageNode().render(Context({
            'snapengage_secure_connection': True}))
        assert 'SnapABug.setSecureConnexion();' in r
        with override_settings(SNAPENGAGE_SECURE_CONNECTION=True):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setSecureConnexion();' in r

    def test_show_offline(self):
        r = SnapEngageNode().render(Context({
            'snapengage_show_offline': False,
        }))
        assert 'SnapABug.allowOffline(false);' in r
        with override_settings(SNAPENGAGE_SHOW_OFFLINE=False):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.allowOffline(false);' in r

    def test_proactive_chat(self):
        r = SnapEngageNode().render(Context({
            'snapengage_proactive_chat': False}))
        assert 'SnapABug.allowProactiveChat(false);' in r

    def test_screenshot(self):
        r = SnapEngageNode().render(Context({
            'snapengage_screenshots': False,
        }))
        assert 'SnapABug.allowScreenshot(false);' in r
        with override_settings(SNAPENGAGE_SCREENSHOTS=False):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.allowScreenshot(false);' in r

    def test_offline_screenshots(self):
        r = SnapEngageNode().render(Context({
            'snapengage_offline_screenshots': False,
        }))
        assert 'SnapABug.showScreenshotOption(false);' in r
        with override_settings(SNAPENGAGE_OFFLINE_SCREENSHOTS=False):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.showScreenshotOption(false);' in r

    def test_sounds(self):
        r = SnapEngageNode().render(Context({'snapengage_sounds': False}))
        assert 'SnapABug.allowChatSound(false);' in r
        with override_settings(SNAPENGAGE_SOUNDS=False):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.allowChatSound(false);' in r

    @override_settings(SNAPENGAGE_READONLY_EMAIL=False)
    def test_email(self):
        r = SnapEngageNode().render(Context({
            'snapengage_email': 'test@example.com',
        }))
        assert 'SnapABug.setUserEmail("test@example.com");' in r

    def test_email_readonly(self):
        r = SnapEngageNode().render(Context({
            'snapengage_email': 'test@example.com',
            'snapengage_readonly_email': True,
        }))
        assert 'SnapABug.setUserEmail("test@example.com",true);' in r
        with override_settings(SNAPENGAGE_READONLY_EMAIL=True):
            r = SnapEngageNode().render(Context({
                'snapengage_email': 'test@example.com',
            }))
            assert 'SnapABug.setUserEmail("test@example.com",true);' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = SnapEngageNode().render(Context({
            'user': User(username='test', email='test@example.com'),
        }))
        assert 'SnapABug.setUserEmail("test@example.com");' in r

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = SnapEngageNode().render(Context({
            'user': AnonymousUser(),
        }))
        assert 'SnapABug.setUserEmail(' not in r

    def test_language(self):
        r = SnapEngageNode().render(Context({'snapengage_locale': 'fr'}))
        assert 'SnapABug.setLocale("fr");' in r
        with override_settings(SNAPENGAGE_LOCALE='fr'):
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setLocale("fr");' in r

    def test_automatic_language(self):
        real_get_language = translation.get_language
        try:
            translation.get_language = lambda: 'fr-ca'
            r = SnapEngageNode().render(Context())
            assert 'SnapABug.setLocale("fr_CA");' in r
        finally:
            translation.get_language = real_get_language

"""
Tests for the SnapEngage template tags and filters.
"""

from django.contrib.auth.models import User, AnonymousUser
from django.template import Context
from django.utils import translation

from analytical.templatetags.snapengage import SnapEngageNode, \
        BUTTON_STYLE_LIVE, BUTTON_STYLE_DEFAULT, BUTTON_STYLE_NONE, \
        BUTTON_LOCATION_LEFT, BUTTON_LOCATION_RIGHT, BUTTON_LOCATION_TOP, \
        BUTTON_LOCATION_BOTTOM, FORM_POSITION_TOP_LEFT
from analytical.tests.utils import TagTestCase, override_settings, \
        SETTING_DELETED
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
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
            '"55%");' in r, r)

    def test_node(self):
        r = SnapEngageNode().render(Context())
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
            '"55%");' in r, r)

    @override_settings(SNAPENGAGE_WIDGET_ID=SETTING_DELETED)
    def test_no_site_id(self):
        self.assertRaises(AnalyticalException, SnapEngageNode)

    @override_settings(SNAPENGAGE_WIDGET_ID='abc')
    def test_wrong_site_id(self):
        self.assertRaises(AnalyticalException, SnapEngageNode)

    def test_no_button(self):
        r = SnapEngageNode().render(Context({'snapengage_button': BUTTON_STYLE_NONE}))
        self.assertTrue('SnapABug.init("ec329c69-0bf0-4db8-9b77-3f8150fb977e")'
                in r, r)
        with override_settings(SNAPENGAGE_BUTTON=BUTTON_STYLE_NONE):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.init("ec329c69-0bf0-4db8-9b77-3f8150fb977e")' in r, r)

    def test_live_button(self):
        r = SnapEngageNode().render(Context({'snapengage_button': BUTTON_STYLE_LIVE}))
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
            '"55%",true);' in r, r)
        with override_settings(SNAPENGAGE_BUTTON=BUTTON_STYLE_LIVE):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
                '"55%",true);' in r, r)

    def test_custom_button(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button': "http://www.example.com/button.png"}))
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
            '"55%");' in r, r)
        self.assertTrue(
            'SnapABug.setButton("http://www.example.com/button.png");' in r, r)
        with override_settings(
                SNAPENGAGE_BUTTON="http://www.example.com/button.png"):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
                '"55%");' in r, r)
            self.assertTrue(
                'SnapABug.setButton("http://www.example.com/button.png");' in r,
                r)

    def test_button_location_right(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location': BUTTON_LOCATION_RIGHT}))
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","1",'
            '"55%");' in r, r)
        with override_settings(
            SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_RIGHT):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","1",'
                '"55%");' in r, r)

    def test_button_location_top(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location': BUTTON_LOCATION_TOP}))
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","2",'
            '"55%");' in r, r)
        with override_settings(SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_TOP):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","2",'
                '"55%");' in r, r)

    def test_button_location_bottom(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location': BUTTON_LOCATION_BOTTOM}))
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","3",'
            '"55%");' in r, r)
        with override_settings(
                SNAPENGAGE_BUTTON_LOCATION=BUTTON_LOCATION_BOTTOM):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","3",'
                '"55%");' in r, r)

    def test_button_offset(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_location_offset': "30%"}))
        self.assertTrue(
            'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
            '"30%");' in r, r)
        with override_settings(SNAPENGAGE_BUTTON_LOCATION_OFFSET="30%"):
            r = SnapEngageNode().render(Context())
            self.assertTrue(
                'SnapABug.addButton("ec329c69-0bf0-4db8-9b77-3f8150fb977e","0",'
                '"30%");' in r, r)

    def test_button_effect(self):
        r = SnapEngageNode().render(Context({
            'snapengage_button_effect': "-4px"}))
        self.assertTrue('SnapABug.setButtonEffect("-4px");' in r, r)
        with override_settings(SNAPENGAGE_BUTTON_EFFECT="-4px"):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setButtonEffect("-4px");' in r, r)

    def test_form_position(self):
        r = SnapEngageNode().render(Context({
            'snapengage_form_position': FORM_POSITION_TOP_LEFT}))
        self.assertTrue('SnapABug.setChatFormPosition("tl");' in r, r)
        with override_settings(SNAPENGAGE_FORM_POSITION=FORM_POSITION_TOP_LEFT):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setChatFormPosition("tl");' in r, r)

    def test_form_top_position(self):
        r = SnapEngageNode().render(Context({
            'snapengage_form_top_position': 40}))
        self.assertTrue('SnapABug.setFormTopPosition(40);' in r, r)
        with override_settings(SNAPENGAGE_FORM_TOP_POSITION=40):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setFormTopPosition(40);' in r, r)

    def test_domain(self):
        r = SnapEngageNode().render(Context({
            'snapengage_domain': "example.com"}))
        self.assertTrue('SnapABug.setDomain("example.com");' in r, r)
        with override_settings(SNAPENGAGE_DOMAIN="example.com"):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setDomain("example.com");' in r, r)

    def test_secure_connection(self):
        r = SnapEngageNode().render(Context({
            'snapengage_secure_connection': True}))
        self.assertTrue('SnapABug.setSecureConnexion();' in r, r)
        with override_settings(SNAPENGAGE_SECURE_CONNECTION=True):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setSecureConnexion();' in r, r)

    def test_show_offline(self):
        r = SnapEngageNode().render(Context({'snapengage_show_offline': False}))
        self.assertTrue('SnapABug.allowOffline(false);' in r, r)
        with override_settings(SNAPENGAGE_SHOW_OFFLINE=False):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.allowOffline(false);' in r, r)

    def test_proactive_chat(self):
        r = SnapEngageNode().render(Context({
            'snapengage_proactive_chat': False}))
        self.assertTrue('SnapABug.allowProactiveChat(false);' in r, r)

    def test_screenshot(self):
        r = SnapEngageNode().render(Context({'snapengage_screenshots': False}))
        self.assertTrue('SnapABug.allowScreenshot(false);' in r, r)
        with override_settings(SNAPENGAGE_SCREENSHOTS=False):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.allowScreenshot(false);' in r, r)

    def test_offline_screenshots(self):
        r = SnapEngageNode().render(Context(
                {'snapengage_offline_screenshots': False}))
        self.assertTrue('SnapABug.showScreenshotOption(false);' in r, r)
        with override_settings(SNAPENGAGE_OFFLINE_SCREENSHOTS=False):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.showScreenshotOption(false);' in r, r)

    def test_sounds(self):
        r = SnapEngageNode().render(Context({'snapengage_sounds': False}))
        self.assertTrue('SnapABug.allowChatSound(false);' in r, r)
        with override_settings(SNAPENGAGE_SOUNDS=False):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.allowChatSound(false);' in r, r)

    @override_settings(SNAPENGAGE_READONLY_EMAIL=False)
    def test_email(self):
        r = SnapEngageNode().render(Context({'snapengage_email':
                'test@example.com'}))
        self.assertTrue('SnapABug.setUserEmail("test@example.com");' in r, r)

    def test_email_readonly(self):
        r = SnapEngageNode().render(Context({'snapengage_email':
                'test@example.com', 'snapengage_readonly_email': True}))
        self.assertTrue('SnapABug.setUserEmail("test@example.com",true);' in r,
                r)
        with override_settings(SNAPENGAGE_READONLY_EMAIL=True):
            r = SnapEngageNode().render(Context({'snapengage_email':
                    'test@example.com'}))
            self.assertTrue('SnapABug.setUserEmail("test@example.com",true);'
                    in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify(self):
        r = SnapEngageNode().render(Context({'user':
                User(username='test', email='test@example.com')}))
        self.assertTrue('SnapABug.setUserEmail("test@example.com");' in r, r)

    @override_settings(ANALYTICAL_AUTO_IDENTIFY=True)
    def test_identify_anonymous_user(self):
        r = SnapEngageNode().render(Context({'user': AnonymousUser()}))
        self.assertFalse('SnapABug.setUserEmail(' in r, r)

    def test_language(self):
        r = SnapEngageNode().render(Context({'snapengage_locale': 'fr'}))
        self.assertTrue('SnapABug.setLocale("fr");' in r, r)
        with override_settings(SNAPENGAGE_LOCALE='fr'):
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setLocale("fr");' in r, r)

    def test_automatic_language(self):
        real_get_language = translation.get_language
        try:
            translation.get_language = lambda: 'fr-ca'
            r = SnapEngageNode().render(Context())
            self.assertTrue('SnapABug.setLocale("fr_CA");' in r, r)
        finally:
            translation.get_language = real_get_language

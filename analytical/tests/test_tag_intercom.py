"""
Tests for the intercom template tags and filters.
"""

import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.intercom import IntercomNode
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(INTERCOM_APP_ID='1234567890abcdef0123456789')
class IntercomTagTestCase(TagTestCase):
    """
    Tests for the ``intercom`` template tag.
    """

    def test_tag(self):
        rendered_tag = self.render_tag('intercom', 'intercom')
        self.assertTrue(rendered_tag.startswith('<!-- Intercom disabled on internal IP address'))

    def test_node(self):
        now = datetime.datetime(2014, 4, 9, 15, 15, 0)
        rendered_tag = IntercomNode().render(Context({
            'user': User(
                username='test',
                first_name='Firstname',
                last_name='Lastname',
                email="test@example.com",
                date_joined=now)
        }))
        # Because the json isn't predictably ordered, we can't just test the whole thing verbatim.
        self.assertEqual("""
<script id="IntercomSettingsScriptTag">
  window.intercomSettings = {"app_id": "1234567890abcdef0123456789", "created_at": 1397074500, "email": "test@example.com", "name": "Firstname Lastname"};
</script>
<script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',intercomSettings);}else{var d=document;var i=function(){i.c(arguments)};i.q=[];i.c=function(args){i.q.push(args)};w.Intercom=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://static.intercomcdn.com/intercom.v1.js';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})()</script>
""", rendered_tag)

    @override_settings(INTERCOM_APP_ID=None)
    def test_no_account_number(self):
        self.assertRaises(AnalyticalException, IntercomNode)

    @override_settings(INTERCOM_APP_ID='123abQ')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, IntercomNode)

    def test_identify_name_email_and_created_at(self):
        now = datetime.datetime(2014, 4, 9, 15, 15, 0)
        r = IntercomNode().render(Context({'user': User(username='test',
                first_name='Firstname', last_name='Lastname',
                email="test@example.com", date_joined=now)}))
        self.assertTrue(
            """window.intercomSettings = {"app_id": "1234567890abcdef0123456789", "created_at": 1397074500, "email": "test@example.com", "name": "Firstname Lastname"};"""\
            in r
        )

    def test_custom(self):
        r = IntercomNode().render(Context({
                'intercom_var1': 'val1',
                'intercom_var2': 'val2'
        }))
        self.assertTrue('var1": "val1", "var2": "val2"' in r)

    def test_identify_name_and_email(self):
        r = IntercomNode().render(Context({
                'user': User(username='test',
                first_name='Firstname',
                last_name='Lastname',
                email="test@example.com")
        }))
        self.assertTrue('"email": "test@example.com", "name": "Firstname Lastname"' in r)

    def test_identify_username_no_email(self):
        r = IntercomNode().render(Context({'user': User(username='test')}))
        self.assertTrue('"name": "test"' in r, r)

    def test_no_identify_when_explicit_name(self):
        r = IntercomNode().render(Context({'intercom_name': 'explicit',
                'user': User(username='implicit')}))
        self.assertTrue('"name": "explicit"' in r, r)

    def test_no_identify_when_explicit_email(self):
        r = IntercomNode().render(Context({'intercom_email': 'explicit',
                'user': User(username='implicit')}))
        self.assertTrue('"email": "explicit"' in r, r)

    def test_disable_for_anonymous_users(self):
        r = IntercomNode().render(Context({'user': AnonymousUser()}))
        self.assertTrue(r.startswith('<!-- Intercom disabled on internal IP address'), r)

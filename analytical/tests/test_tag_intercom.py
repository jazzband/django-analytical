"""
Tests for the intercom template tags and filters.
"""

import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.template import Context

from analytical.templatetags.intercom import IntercomNode
from analytical.tests.utils import TagTestCase, override_settings, SETTING_DELETED
from analytical.utils import AnalyticalException


@override_settings(INTERCOM_APP_ID='1234567890abcdef0123456789')
class IntercomTagTestCase(TagTestCase):
    """
    Tests for the ``intercom`` template tag.
    """

    def test_tag(self):
        self.assertEqual("""<!-- Intercom disabled on internal IP address

-->""",
                self.render_tag('intercom', 'intercom'))

    def test_node(self):
        now = datetime.datetime(2014, 4, 9, 15, 15, 0)
        self.assertEqual(
                """
<script id="IntercomSettingsScriptTag">
  window.intercomSettings = {'app_id': '1234567890abcdef0123456789', 'full_name': 'Firstname Lastname', 'email': 'test@example.com', 'created_at': 1397074500};
</script>
<script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',intercomSettings);}else{var d=document;var i=function(){i.c(arguments)};i.q=[];i.c=function(args){i.q.push(args)};w.Intercom=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://static.intercomcdn.com/intercom.v1.js';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})()</script>
""",
                IntercomNode().render(Context({
                    'user': User(
                        username='test',
                        first_name='Firstname',
                        last_name='Lastname',
                        email="test@example.com",
                        date_joined=now)
                }))
        )

    @override_settings(INTERCOM_APP_ID=SETTING_DELETED)
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
        self.assertTrue("window.intercomSettings = {'app_id': '1234567890abcdef0123456789', "
                "'full_name': 'Firstname Lastname', "
                "'email': 'test@example.com', 'created_at': 1397074500};" in r, r)

    def test_disable_for_anonymous_users(self):
        r = IntercomNode().render(Context({'user': AnonymousUser()}))
        self.assertTrue(r.startswith('<!-- Intercom disabled on internal IP address'), r)

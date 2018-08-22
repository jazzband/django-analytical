"""
Tests for the intercom template tags and filters.
"""

import datetime

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings

from analytical.templatetags.intercom import IntercomNode, intercom_user_hash, _timestamp
from analytical.tests.utils import TagTestCase
from analytical.utils import AnalyticalException


@override_settings(INTERCOM_APP_ID="abc123xyz")
class IntercomTagTestCase(TagTestCase):
    """
    Tests for the ``intercom`` template tag.
    """

    def test_tag(self):
        rendered_tag = self.render_tag('intercom', 'intercom')
        self.assertTrue(rendered_tag.strip().startswith('<script id="IntercomSettingsScriptTag">'))

    def test_node(self):
        now = datetime.datetime(2014, 4, 9, 15, 15, 0)
        user = User.objects.create(
            username='test',
            first_name='Firstname',
            last_name='Lastname',
            email="test@example.com",
            date_joined=now,
        )
        rendered_tag = IntercomNode().render(Context({'user': user}))
        # Because the json isn't predictably ordered, we can't just test the whole thing verbatim.
        self.assertEqual("""
<script id="IntercomSettingsScriptTag">
  window.intercomSettings = {"app_id": "abc123xyz", "created_at": 1397074500, "email": "test@example.com", "name": "Firstname Lastname", "user_id": %(user_id)s};
</script>
<script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',intercomSettings);}else{var d=document;var i=function(){i.c(arguments)};i.q=[];i.c=function(args){i.q.push(args)};w.Intercom=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://static.intercomcdn.com/intercom.v1.js';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})()</script>
""" % {'user_id': user.pk}, rendered_tag)  # noqa

    @override_settings(INTERCOM_APP_ID=None)
    def test_no_account_number(self):
        self.assertRaises(AnalyticalException, IntercomNode)

    @override_settings(INTERCOM_APP_ID='123abQ')
    def test_wrong_account_number(self):
        self.assertRaises(AnalyticalException, IntercomNode)

    def test_identify_name_email_and_created_at(self):
        now = datetime.datetime(2014, 4, 9, 15, 15, 0)
        user = User.objects.create(
            username='test',
            first_name='Firstname',
            last_name='Lastname',
            email="test@example.com",
            date_joined=now,
        )
        r = IntercomNode().render(Context({
            'user': user,
        }))
        self.assertTrue('window.intercomSettings = {'
                        '"app_id": "abc123xyz", "created_at": 1397074500, '
                        '"email": "test@example.com", "name": "Firstname Lastname", '
                        '"user_id": %(user_id)s'
                        '};' % {'user_id': user.pk} in r, msg=r)

    def test_custom(self):
        r = IntercomNode().render(Context({
                'intercom_var1': 'val1',
                'intercom_var2': 'val2'
        }))
        self.assertTrue('var1": "val1", "var2": "val2"' in r)

    def test_identify_name_and_email(self):
        r = IntercomNode().render(Context({
                'user': User(
                    username='test',
                    first_name='Firstname',
                    last_name='Lastname',
                    email="test@example.com"),
        }))
        self.assertTrue('"email": "test@example.com", "name": "Firstname Lastname"' in r)

    def test_identify_username_no_email(self):
        r = IntercomNode().render(Context({'user': User(username='test')}))
        self.assertTrue('"name": "test"' in r, r)

    def test_no_identify_when_explicit_name(self):
        r = IntercomNode().render(Context({
            'intercom_name': 'explicit',
            'user': User(username='implicit'),
        }))
        self.assertTrue('"name": "explicit"' in r, r)

    def test_no_identify_when_explicit_email(self):
        r = IntercomNode().render(Context({
            'intercom_email': 'explicit',
            'user': User(username='implicit'),
        }))
        self.assertTrue('"email": "explicit"' in r, r)

    @override_settings(INTERCOM_HMAC_SECRET_KEY='secret')
    def test_user_hash__without_user_details(self):
        """
        No `user_hash` without `user_id` or `email`.
        """
        attrs = IntercomNode()._get_custom_attrs(Context())
        self.assertEqual({
            'created_at': None,
        }, attrs)

    @override_settings(INTERCOM_HMAC_SECRET_KEY='secret')
    def test_user_hash__with_user(self):
        """
        'user_hash' of default `user_id`.
        """
        user = User.objects.create(
            email='test@example.com',
        )  # type: User
        attrs = IntercomNode()._get_custom_attrs(Context({'user': user}))
        self.assertEqual({
            'created_at': int(_timestamp(user.date_joined)),
            'email': 'test@example.com',
            'name': '',
            'user_hash': intercom_user_hash(str(user.pk)),
            'user_id': user.pk,
        }, attrs)

    @override_settings(INTERCOM_HMAC_SECRET_KEY='secret')
    def test_user_hash__with_explicit_user_id(self):
        """
        'user_hash' of context-provided `user_id`.
        """
        attrs = IntercomNode()._get_custom_attrs(Context({
            'intercom_email': 'test@example.com',
            'intercom_user_id': '5',
        }))
        self.assertEqual({
            'created_at': None,
            'email': 'test@example.com',
            # HMAC for user_id:
            'user_hash': 'd3123a7052b42272d9b520235008c248a5aff3221cc0c530b754702ad91ab102',
            'user_id': '5',
        }, attrs)

    @override_settings(INTERCOM_HMAC_SECRET_KEY='secret')
    def test_user_hash__with_explicit_email(self):
        """
        'user_hash' of context-provided `email`.
        """
        attrs = IntercomNode()._get_custom_attrs(Context({
            'intercom_email': 'test@example.com',
        }))
        self.assertEqual({
            'created_at': None,
            'email': 'test@example.com',
            # HMAC for email:
            'user_hash': '49e43229ee99dca2565241719b8341b04e71dd4de0628f991b5bea30a526e153',
        }, attrs)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = IntercomNode().render(context)
        self.assertTrue(r.startswith('<!-- Intercom disabled on internal IP address'), r)
        self.assertTrue(r.endswith('-->'), r)

"""
Tests for the analytical.utils module.
"""
# import django

import pytest
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TestCase

from analytical.utils import (
    AnalyticalException,
    get_domain,
    get_identity,
    get_required_setting,
    is_internal_ip,
)


class SettingDeletedTestCase(TestCase):
    @override_settings(USER_ID=None)
    def test_get_required_setting(self):
        """
        Make sure using get_required_setting fails in the right place.
        """

        with pytest.raises(AnalyticalException, match='USER_ID setting is not set'):
            get_required_setting('USER_ID', r'\d+', 'invalid USER_ID')


class MyUser(AbstractBaseUser):
    identity = models.CharField(max_length=50)
    USERNAME_FIELD = 'identity'

    class Meta:
        abstract = False
        app_label = 'testapp'


class GetIdentityTestCase(TestCase):
    def test_custom_username_field(self):
        get_id = get_identity(Context({}), user=MyUser(identity='fake_id'))
        assert get_id == 'fake_id'

    def test_custom_identity_specific_provider(self):
        get_id = get_identity(
            Context(
                {
                    'foo_provider_identity': 'bar',
                    'analytical_identity': 'baz',
                }
            ),
            prefix='foo_provider',
        )
        assert get_id == 'bar'

    def test_custom_identity_general(self):
        get_id = get_identity(
            Context(
                {
                    'analytical_identity': 'baz',
                }
            ),
            prefix='foo_provider',
        )
        assert get_id == 'baz'


@override_settings(ANALYTICAL_DOMAIN='example.org')
class GetDomainTestCase(TestCase):
    def test_get_service_domain_from_context(self):
        context = Context({'test_domain': 'example.com'})
        assert get_domain(context, 'test') == 'example.com'

    def test_get_analytical_domain_from_context(self):
        context = Context({'analytical_domain': 'example.com'})
        assert get_domain(context, 'test') == 'example.com'

    @override_settings(TEST_DOMAIN='example.net')
    def test_get_service_domain_from_settings(self):
        context = Context()
        assert get_domain(context, 'test') == 'example.net'

    def test_get_analytical_domain_from_settings(self):
        context = Context()
        assert get_domain(context, 'test') == 'example.org'


# FIXME: enable Django apps dynamically and enable test again
# @with_apps('django.contrib.sites')
# @override_settings(TEST_DOMAIN=SETTING_DELETED, ANALYTICAL_DOMAIN=SETTING_DELETED)
# class GetDomainTestCaseWithSites(TestCase):
#    def test_get_domain_from_site(self):
#        site = Site.objects.create(domain="example.com", name="test")
#        with override_settings(SITE_ID=site.id):
#            context = Context()
#            self.assertEqual(get_domain(context, 'test'), 'example.com')


class InternalIpTestCase(TestCase):
    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_no_internal_ip(self):
        context = Context()
        assert not is_internal_ip(context)

    @override_settings(INTERNAL_IPS=['1.1.1.1'])
    @override_settings(ANALYTICAL_INTERNAL_IPS=[])
    def test_render_analytical_internal_ips_override_when_empty(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        assert not is_internal_ip(context)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        assert is_internal_ip(context)

    @override_settings(TEST_INTERNAL_IPS=['1.1.1.1'])
    def test_render_prefix_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        assert is_internal_ip(context, 'TEST')

    @override_settings(INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip_fallback(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        assert is_internal_ip(context)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip_forwarded_for(self):
        req = HttpRequest()
        req.META['HTTP_X_FORWARDED_FOR'] = '1.1.1.1'
        context = Context({'request': req})
        assert is_internal_ip(context)

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_different_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '2.2.2.2'
        context = Context({'request': req})
        assert not is_internal_ip(context)

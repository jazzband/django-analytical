"""
Tests for the base service.
"""

import re

from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.test import TestCase

from analytical.services.base import AnalyticalService
from analytical.tests.utils import TestSettingsManager


class DummyService(AnalyticalService):
    def render_test(self, context):
        return context


class BaseServiceTestCase(TestCase):
    """
    Tests for the base service.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()
        self.service = DummyService()

    def tearDown(self):
        self.settings_manager.revert()

    def test_render(self):
        r = self.service.render('test', 'foo')
        self.assertEqual('foo', r)

    def test_get_required_setting(self):
        self.settings_manager.set(TEST='test')
        r = self.service.get_required_setting('TEST', re.compile('es'), 'fail')
        self.assertEqual('test', r)

    def test_get_required_setting_missing(self):
        self.settings_manager.delete('TEST')
        self.assertRaises(ImproperlyConfigured,
                self.service.get_required_setting, 'TEST', re.compile('es'),
                'fail')

    def test_get_required_setting_wrong(self):
        self.settings_manager.set(TEST='test')
        self.assertRaises(ImproperlyConfigured,
                self.service.get_required_setting, 'TEST', re.compile('foo'),
                'fail')

    def test_get_identity_none(self):
        context = {}
        self.assertEqual(None, self.service.get_identity(context))

    def test_get_identity_authenticated(self):
        context = {'user': User(username='test')}
        self.assertEqual('test', self.service.get_identity(context))

    def test_get_identity_authenticated_request(self):
        req = HttpRequest()
        req.user = User(username='test')
        context = {'request': req}
        self.assertEqual('test', self.service.get_identity(context))

    def test_get_identity_anonymous(self):
        context = {'user': AnonymousUser()}
        self.assertEqual(None, self.service.get_identity(context))

    def test_get_identity_non_user(self):
        context = {'user': object()}
        self.assertEqual(None, self.service.get_identity(context))

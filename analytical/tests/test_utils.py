"""
Tests for the analytical.utils module.
"""

from django.http import HttpRequest
from django.template import Context

from analytical.utils import is_internal_ip
from analytical.tests.utils import TestCase


class InternalIpTestCase(TestCase):
    def test_render_no_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        context = Context()
        self.assertFalse(is_internal_ip(context))

    def test_render_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        self.assertTrue(is_internal_ip(context))

    def test_render_prefix_internal_ip(self):
        self.settings_manager.set(TEST_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        self.assertTrue(is_internal_ip(context, 'TEST'))

    def test_render_internal_ip_fallback(self):
        self.settings_manager.set(INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        self.assertTrue(is_internal_ip(context))

    def test_render_internal_ip_forwarded_for(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['HTTP_X_FORWARDED_FOR'] = '1.1.1.1'
        context = Context({'request': req})
        self.assertTrue(is_internal_ip(context))

    def test_render_different_internal_ip(self):
        self.settings_manager.set(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '2.2.2.2'
        context = Context({'request': req})
        self.assertFalse(is_internal_ip(context))

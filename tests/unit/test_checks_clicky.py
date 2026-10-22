"""System checks for Clicky's optional domain validation."""

from io import StringIO

import pytest
from django.core import checks
from django.core.management import call_command
from django.test.utils import override_settings


def clicky_checks():
    return [
        message
        for message in checks.run_checks(tags=[checks.Tags.security])
        if message.id == 'analytical.W001'
    ]


@pytest.mark.parametrize(
    'policy',
    [
        'same-origin',
        'no-referrer',
        ['origin', 'same-origin'],
        ['origin', ' same-origin '],
        ['origin, same-origin'],
        'origin, no-referrer',
        'same-origin, unknown-policy',
    ],
)
@override_settings(
    CLICKY_SITE_ID='12345678',
    MIDDLEWARE=['django.middleware.security.SecurityMiddleware'],
)
def test_clicky_check_warns_for_restrictive_policy(policy):
    with override_settings(SECURE_REFERRER_POLICY=policy):
        messages = clicky_checks()
    assert len(messages) == 1
    assert isinstance(messages[0], checks.Warning)
    assert 'domain validation' in messages[0].msg
    assert 'SECURE_REFERRER_POLICY' in messages[0].hint


@pytest.mark.parametrize(
    'policy',
    [
        None,
        '',
        [],
        'origin',
        'origin-when-cross-origin',
        'strict-origin-when-cross-origin',
        ['same-origin', 'origin'],
        'no-referrer, origin-when-cross-origin',
    ],
)
@override_settings(
    CLICKY_SITE_ID='12345678',
    MIDDLEWARE=['django.middleware.security.SecurityMiddleware'],
)
def test_clicky_check_allows_referrer_policy(policy):
    with override_settings(SECURE_REFERRER_POLICY=policy):
        assert clicky_checks() == []


@pytest.mark.parametrize('site_id', [None, ''])
@override_settings(
    SECURE_REFERRER_POLICY='same-origin',
    MIDDLEWARE=['django.middleware.security.SecurityMiddleware'],
)
def test_clicky_check_ignores_unconfigured_clicky(site_id):
    with override_settings(CLICKY_SITE_ID=site_id):
        assert clicky_checks() == []


@pytest.mark.parametrize(
    'middleware', [[], ['django.middleware.common.CommonMiddleware']]
)
@override_settings(CLICKY_SITE_ID='12345678', SECURE_REFERRER_POLICY='same-origin')
def test_clicky_check_ignores_missing_security_middleware(middleware):
    with override_settings(MIDDLEWARE=middleware):
        assert clicky_checks() == []


@override_settings(
    CLICKY_SITE_ID='12345678',
    SECURE_REFERRER_POLICY='same-origin',
    MIDDLEWARE=['django.middleware.security.SecurityMiddleware'],
)
def test_clicky_check_can_be_silenced():
    stderr = StringIO()
    call_command('check', tags=['security'], stderr=stderr)
    assert 'analytical.W001' in stderr.getvalue()
    stderr = StringIO()
    with override_settings(SILENCED_SYSTEM_CHECKS=['analytical.W001']):
        call_command('check', tags=['security'], stderr=stderr)
    assert 'analytical.W001' not in stderr.getvalue()

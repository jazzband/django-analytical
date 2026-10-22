"""System checks for Clicky's optional domain validation."""

import json
import subprocess
import sys
import warnings
from io import StringIO
from pathlib import Path

import pytest
from django.core import checks
from django.core.management import call_command
from django.test.utils import override_settings
from utils import TagTestCase


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


@override_settings(CLICKY_SITE_ID='12345678', SECURE_REFERRER_POLICY='same-origin')
def test_clicky_render_does_not_emit_runtime_warnings():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        for _ in range(2):
            assert 'clicky_site_ids.push(12345678)' in TagTestCase().render_tag(
                'clicky', 'clicky'
            )
    assert not caught


def test_clicky_check_registered_on_application_startup():
    result = subprocess.run(
        [
            sys.executable,
            '-c',
            "import os; os.environ['DJANGO_SETTINGS_MODULE'] = "
            "'tests.testproject.settings'; import django; django.setup(); "
            'import json; from django.core import checks; '
            'from django.test.utils import override_settings; '
            "settings = override_settings(CLICKY_SITE_ID='12345678', "
            "SECURE_REFERRER_POLICY='same-origin', "
            "MIDDLEWARE=['django.middleware.security.SecurityMiddleware']); "
            'settings.enable(); '
            'print(json.dumps([m.id for m in '
            'checks.run_checks(tags=[checks.Tags.security]) '
            "if m.id.startswith('analytical.')]))",
        ],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == ['analytical.W001']

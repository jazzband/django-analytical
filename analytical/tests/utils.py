"""
Testing utilities.
"""

from __future__ import with_statement
from django.conf import settings, UserSettingsHolder
from django.core.management import call_command
from django.db.models import loading
from django.template import Template, Context, RequestContext
from django.test.simple import run_tests as django_run_tests
from django.test.testcases import TestCase as DjangoTestCase
from django.utils.functional import wraps

class override_settings(object):
    """
    Acts as either a decorator, or a context manager.  If it's a decorator it
    takes a function and returns a wrapped function.  If it's a contextmanager
    it's used with the ``with`` statement.  In either event entering/exiting
    are called before and after, respectively, the function/block is executed.

    Via: http://djangosnippets.org/snippets/2437/
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.wrapped = settings._wrapped

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def enable(self):
        override = UserSettingsHolder(settings._wrapped)
        for key, new_value in self.options.items():
            setattr(override, key, new_value)
        settings._wrapped = override

    def disable(self):
        settings._wrapped = self.wrapped

def run_tests(labels=()):
    """
    Use the Django test runner to run the tests.
    """
    django_run_tests(labels, verbosity=1, interactive=True)


class TestCase(DjangoTestCase):
    """
    Base test case for the django-analytical tests.

    Includes the settings manager.
    """

    def setUp(self):
        self.settings_manager = TestSettingsManager()

    def tearDown(self):
        self.settings_manager.revert()


class TagTestCase(TestCase):
    """
    Tests for a template tag.

    Includes the settings manager.
    """

    def render_tag(self, library, tag, vars=None, request=None):
        if vars is None:
            vars = {}
        t = Template("{%% load %s %%}{%% %s %%}" % (library, tag))
        if request is not None:
            context = RequestContext(request, vars)
        else:
            context = Context(vars)
        return t.render(context)


class TestSettingsManager(object):
    """
    From: http://www.djangosnippets.org/snippets/1011/

    A class which can modify some Django settings temporarily for a
    test and then revert them to their original values later.

    Automatically handles resyncing the DB if INSTALLED_APPS is
    modified.
    """

    NO_SETTING = ('!', None)

    def __init__(self):
        self._original_settings = {}

    def set(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._original_settings.setdefault(k, getattr(settings, k,
                    self.NO_SETTING))
            setattr(settings, k, v)
        if 'INSTALLED_APPS' in kwargs:
            self.syncdb()

    def delete(self, *args):
        for k in args:
            try:
                self._original_settings.setdefault(k, getattr(settings, k,
                        self.NO_SETTING))
                delattr(settings, k)
            except AttributeError:
                pass  # setting did not exist

    def syncdb(self):
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0, interactive=False)

    def revert(self):
        for k,v in self._original_settings.iteritems():
            if v == self.NO_SETTING:
                if hasattr(settings, k):
                    delattr(settings, k)
            else:
                setattr(settings, k, v)
        if 'INSTALLED_APPS' in self._original_settings:
            self.syncdb()
        self._original_settings = {}

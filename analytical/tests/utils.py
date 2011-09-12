"""
Testing utilities.
"""

from __future__ import with_statement

from django.conf import settings, UserSettingsHolder
from django.core.management import call_command
from django.db.models import loading
from django.template import Template, Context, RequestContext
from django.test.testcases import TestCase
from django.utils.functional import wraps


SETTING_DELETED = object()


# Backported adapted from Django trunk (r16377)
class override_settings(object):
    """
    Temporarily override Django settings.

    Acts as either a decorator, or a context manager.  If it's a decorator it
    takes a function and returns a wrapped function.  If it's a contextmanager
    it's used with the ``with`` statement.  In either event entering/exiting
    are called before and after, respectively, the function/block is executed.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.wrapped = settings._wrapped

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        from django.test import TransactionTestCase
        if isinstance(test_func, type) and issubclass(test_func, TransactionTestCase):
            # When decorating a class, we need to construct a new class
            # with the same name so that the test discovery tools can
            # get a useful name.
            def _pre_setup(innerself):
                self.enable()
                test_func._pre_setup(innerself)
            def _post_teardown(innerself):
                test_func._post_teardown(innerself)
                self.disable()
            inner = type(
                test_func.__name__,
                (test_func,),
                {
                    '_pre_setup': _pre_setup,
                    '_post_teardown': _post_teardown,
                    '__module__': test_func.__module__,
                })
        else:
            @wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def enable(self):
        override = UserSettingsHolder(settings._wrapped)
        for key, new_value in self.options.items():
            if new_value is SETTING_DELETED:
                delattr(override.default_settings, key)
            else:
                setattr(override, key, new_value)
        settings._wrapped = override

    def disable(self):
        settings._wrapped = self.wrapped


def run_tests():
    """
    Use the Django test runner to run the tests.
    """
    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=2)
    runner.run_tests(None)


def with_apps(*apps):
    """
    Class decorator that makes sure the passed apps are present in
    INSTALLED_APPS.
    """
    apps_set = set(settings.INSTALLED_APPS)
    apps_set.update(apps)
    return override_settings(INSTALLED_APPS=list(apps_set))


def without_apps(*apps):
    """
    Class decorator that makes sure the passed apps are not present in
    INSTALLED_APPS.
    """
    apps_list = [a for a in settings.INSTALLED_APPS if a not in apps]
    return override_settings(INSTALLED_APPS=apps_list)


class TagTestCase(TestCase):
    """
    Tests for a template tag.

    Adds support methods for testing template tags.
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

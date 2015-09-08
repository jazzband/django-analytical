"""
Testing utilities.
"""

from __future__ import with_statement

from django.template import Template, Context, RequestContext
from django.test.testcases import TestCase


def run_tests():
    """
    Use the Django test runner to run the tests.

    Sets the return code to the number of failed tests.
    """
    import sys
    import django
    try:
        django.setup()
    except AttributeError:
        pass
    try:
        from django.test.runner import DiscoverRunner as TestRunner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner as TestRunner
    runner = TestRunner()
    sys.exit(runner.run_tests(["analytical"]))


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

    def render_template(self, template, vars=None, request=None):
        if vars is None:
            vars = {}
        t = Template(template)
        if request is not None:
            context = RequestContext(request, vars)
        else:
            context = Context(vars)
        return t.render(context)

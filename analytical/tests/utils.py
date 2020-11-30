"""
Testing utilities.
"""

from __future__ import with_statement

from django.template import Template, Context, RequestContext
from django.test.testcases import TestCase


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

#
# This file is execfile()d with the current directory set to its containing
# directory.

import os
import sys

sys.path.append(os.path.join(os.path.abspath('.'), '_ext'))
sys.path.append(os.path.dirname(os.path.abspath('.')))

import analytical  # noqa

# -- General configuration --------------------------------------------------

project = 'django-analytical'
copyright = '2011, Joost Cassee <joost@cassee.net>'

release = analytical.__version__
# The short X.Y version.
version = release.rsplit('.', 1)[0]

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'local']
templates_path = ['_templates']
source_suffix = {'.rst': 'restructuredtext'}
master_doc = 'index'

add_function_parentheses = True
pygments_style = 'sphinx'

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.13', None),
    'django': ('https://docs.djangoproject.com/en/stable', None),
}


# -- Options for HTML output ------------------------------------------------

html_theme = 'default'
htmlhelp_basename = 'analyticaldoc'


# -- Options for LaTeX output -----------------------------------------------

latex_documents = [
    (
        'index',
        'django-analytical.tex',
        'Documentation for django-analytical',
        'Joost Cassee',
        'manual',
    ),
]

# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its containing
# directory.

import sys, os
sys.path.append(os.path.join(os.path.abspath('.'), '_ext'))
sys.path.append(os.path.dirname(os.path.abspath('.')))

import analytical


# -- General configuration -----------------------------------------------------

project = u'django-analytical'
copyright = u'2011, Joost Cassee <joost@cassee.net>'

release = analytical.__version__
# The short X.Y version.
version = release.rsplit('.', 1)[0]

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'local']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

add_function_parentheses = True
pygments_style = 'sphinx'

intersphinx_mapping = {
    'http://docs.python.org/2.6': None,
    'http://docs.djangoproject.com/en/1.3': 'http://docs.djangoproject.com/en/1.3/_objects/',
}


# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'analyticaldoc'


# -- Options for LaTeX output --------------------------------------------------

latex_documents = [
  ('index', 'django-analytical.tex', u'Documentation for django-analytical',
   u'Joost Cassee', 'manual'),
]

==================================
Matomo (formerly Piwik) -- open source web analytics
==================================

Matomo_ is an open analytics platform currently used by individuals,
companies and governments all over the world.

.. _Matomo: http://matomo.org/


Installation
============

To start using the Matomo integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Matomo template tag to your templates.  This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`matomo-configuration`.

The Matomo tracking code is inserted into templates using a template
tag.  Load the :mod:`matomo` template tag library and insert the
:ttag:`matomo` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body as recommended by the
`Matomo best practice for Integration Plugins`_::

    {% load matomo %}
    ...
    {% matomo %}
    </body>
    </html>

.. _`Matomo best practice for Integration Plugins`: http://matomo.org/integrate/how-to/



.. _matomo-configuration:

Configuration
=============

Before you can use the Matomo integration, you must first define
domain name and optional URI path to your Matomo server, as well as
the Matomo ID of the website you're tracking with your Matomo server,
in your project settings.


Setting the domain
------------------

Your Django project needs to know where your Matomo server is located.
Typically, you'll have Matomo installed on a subdomain of its own
(e.g. ``matomo.example.com``), otherwise it runs in a subdirectory of
a website of yours (e.g. ``www.example.com/matomo``).  Set
:const:`MATOMO_DOMAIN_PATH` in the project :file:`settings.py` file
accordingly::

    MATOMO_DOMAIN_PATH = 'matomo.example.com'

If you do not set a domain the tracking code will not be rendered.


Setting the site ID
-------------------

Your Matomo server can track several websites.  Each website has its
site ID (this is the ``idSite`` parameter in the query string of your
browser's address bar when you visit the Matomo Dashboard).  Set
:const:`MATOMO_SITE_ID` in the project :file:`settings.py` file to
the value corresponding to the website you're tracking::

    MATOMO_SITE_ID = '4'

If you do not set the site ID the tracking code will not be rendered.


.. _matomo-uservars:

User variables
--------------

Matomo supports sending `custom variables`_ along with default statistics. If
you want to set a custom variable, use the context variable ``matomo_vars`` when
you render your template. It should be an iterable of custom variables
represented by tuples like: ``(index, name, value[, scope])``, where scope may
be ``'page'`` (default) or ``'visit'``. ``index`` should be an integer and the
other parameters should be strings. ::

    context = Context({
        'matomo_vars': [(1, 'foo', 'Sir Lancelot of Camelot'),
                        (2, 'bar', 'To seek the Holy Grail', 'page'),
                        (3, 'spam', 'Blue', 'visit')]
    })
    return some_template.render(context)

Matomo default settings allow up to 5 custom variables for both scope. Variable
mapping between index and name must stay constant, or the latest name
override the previous one.

If you use the same user variables in different views and its value can
be computed from the HTTP request, you can also set them in a context
processor that you add to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list
in :file:`settings.py`.

.. _`custom variables`: http://developer.matomo.org/guides/tracking-javascript-guide#custom-variables


.. _matomo-user-tracking:

User tracking
-------------

If you use the standard Django authentication system, you can allow Matomo to
`track individual users`_ by setting the :data:`ANALYTICAL_AUTO_IDENTIFY`
setting to :const:`True`. This is enabled by default. Matomo will identify
users based on their ``username``.

If you disable this settings, or want to customize what user id to use, you can
set the context variable ``analytical_identity`` (for global configuration) or
``matomo_identity`` (for Matomo specific configuration). Setting one to
:const:`None` will disable the user tracking feature::

    # Matomo will identify this user as 'BDFL' if ANALYTICAL_AUTO_IDENTIFY is True or unset
    request.user = User(username='BDFL', first_name='Guido', last_name='van Rossum')

    # Matomo will identify this user as 'Guido van Rossum'
    request.user = User(username='BDFL', first_name='Guido', last_name='van Rossum')
    context = Context({
        'matomo_identity': request.user.get_full_name()
    })

    # Matomo will not identify this user (but will still collect statistics)
    request.user = User(username='BDFL', first_name='Guido', last_name='van Rossum')
    context = Context({
        'matomo_identity': None
    })

.. _`track individual users`: http://developer.matomo.org/guides/tracking-javascript-guide#user-id

Disabling cookies
-----------------

If you want to `disable cookies`_, set :data:`MATOMO_DISABLE_COOKIES` to
:const:`True`. This is disabled by default.

.. _`disable cookies`: https://matomo.org/faq/general/faq_157/

Internal IP addresses
---------------------

Usually, you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`ANALYTICAL_INTERNAL_IPS` (which
takes the value of :const:`INTERNAL_IPS` by default) the tracking code
is commented out.  See :ref:`identifying-visitors` for important
information about detecting the visitor IP address.

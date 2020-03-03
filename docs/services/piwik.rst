==================================
Piwik (deprecated) -- open source web analytics
==================================

Piwik_ is an open analytics platform currently used by individuals,
companies and governments all over the world.  With Piwik, your data
will always be yours, because you run your own analytics server.

.. _Piwik: http://www.piwik.org/


Deprecated
==========

Note that Piwik is now known as Matomo.  New projects should use the
Matomo integration.  The Piwik integration in django-analytical is
deprecated and eventually will be removed.


Installation
============

To start using the Piwik integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Piwik template tag to your templates.  This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`piwik-configuration`.

The Piwik tracking code is inserted into templates using a template
tag.  Load the :mod:`piwik` template tag library and insert the
:ttag:`piwik` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body as recommended by the
`Piwik best practice for Integration Plugins`_::

    {% load piwik %}
    ...
    {% piwik %}
    </body>
    </html>

.. _`Piwik best practice for Integration Plugins`: http://piwik.org/integrate/how-to/



.. _piwik-configuration:

Configuration
=============

Before you can use the Piwik integration, you must first define
domain name and optional URI path to your Piwik server, as well as
the Piwik ID of the website you're tracking with your Piwik server,
in your project settings.


Setting the domain
------------------

Your Django project needs to know where your Piwik server is located.
Typically, you'll have Piwik installed on a subdomain of its own
(e.g. ``piwik.example.com``), otherwise it runs in a subdirectory of
a website of yours (e.g. ``www.example.com/piwik``).  Set
:const:`PIWIK_DOMAIN_PATH` in the project :file:`settings.py` file
accordingly::

    PIWIK_DOMAIN_PATH = 'piwik.example.com'

If you do not set a domain the tracking code will not be rendered.


Setting the site ID
-------------------

Your Piwik server can track several websites.  Each website has its
site ID (this is the ``idSite`` parameter in the query string of your
browser's address bar when you visit the Piwik Dashboard).  Set
:const:`PIWIK_SITE_ID` in the project :file:`settings.py` file to
the value corresponding to the website you're tracking::

    PIWIK_SITE_ID = '4'

If you do not set the site ID the tracking code will not be rendered.


.. _piwik-uservars:

User variables
--------------

Piwik supports sending `custom variables`_ along with default statistics. If
you want to set a custom variable, use the context variable ``piwik_vars`` when
you render your template. It should be an iterable of custom variables
represented by tuples like: ``(index, name, value[, scope])``, where scope may
be ``'page'`` (default) or ``'visit'``. ``index`` should be an integer and the
other parameters should be strings. ::

    context = Context({
        'piwik_vars': [(1, 'foo', 'Sir Lancelot of Camelot'),
                       (2, 'bar', 'To seek the Holy Grail', 'page'),
                       (3, 'spam', 'Blue', 'visit')]
    })
    return some_template.render(context)

Piwik default settings allow up to 5 custom variables for both scope. Variable
mapping between index and name must stay constant, or the latest name
override the previous one.

If you use the same user variables in different views and its value can
be computed from the HTTP request, you can also set them in a context
processor that you add to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list
in :file:`settings.py`.

.. _`custom variables`: http://developer.piwik.org/guides/tracking-javascript-guide#custom-variables


.. _piwik-user-tracking:

User tracking
-------------

If you use the standard Django authentication system, you can allow Piwik to
`track individual users`_ by setting the :data:`ANALYTICAL_AUTO_IDENTIFY`
setting to :const:`True`. This is enabled by default. Piwik will identify
users based on their ``username``.

If you disable this settings, or want to customize what user id to use, you can
set the context variable ``analytical_identity`` (for global configuration) or
``piwik_identity`` (for Piwik specific configuration). Setting one to
:const:`None` will disable the user tracking feature::

    # Piwik will identify this user as 'BDFL' if ANALYTICAL_AUTO_IDENTIFY is True or unset
    request.user = User(username='BDFL', first_name='Guido', last_name='van Rossum')

    # Piwik will identify this user as 'Guido van Rossum'
    request.user = User(username='BDFL', first_name='Guido', last_name='van Rossum')
    context = Context({
        'piwik_identity': request.user.get_full_name()
    })

    # Piwik will not identify this user (but will still collect statistics)
    request.user = User(username='BDFL', first_name='Guido', last_name='van Rossum')
    context = Context({
        'piwik_identity': None
    })

.. _`track individual users`: http://developer.piwik.org/guides/tracking-javascript-guide#user-id

Disabling cookies
-----------------

If you want to `disable cookies`_, set :data:`PIWIKI_DISABLE_COOKIES` to
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


----

Thanks go to Piwik for providing an excellent web analytics platform
entirely for free!  Consider donating_ to ensure that they continue
their development efforts in the spirit of open source and freedom
for our personal data.

.. _donating: http://piwik.org/donate/

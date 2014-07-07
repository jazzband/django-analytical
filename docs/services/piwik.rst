==================================
Piwik -- open source web analytics
==================================

Piwik_ is an open analytics platform currently used by individuals,
companies and governments all over the world.  With Piwik, your data
will always be yours, because you run your own analytics server.

.. _Piwik: http://www.piwik.org/


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

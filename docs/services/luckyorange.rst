==================================================
Lucky Orange -- All-in-one conversion optimization
==================================================

`Lucky Orange`_ is a website analytics and user feedback tool.

.. _`Lucky Orange`: https://www.luckyorange.com/


.. luckyorange-installation:

Installation
============

To start using the Lucky Orange integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Lucky Orange template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`luckyorange-configuration`.

The Lucky Orange tracking code is inserted into templates using template
tags.  Because every page that you want to track must have the tag, it
is useful to add it to your base template.  At the top of the template,
load the :mod:`luckyorange` template tag library.  Then insert the
:ttag:`luckyorange` tag at the bottom of the head section::

    {% load luckyorange %}
    <html>
    <head>
    ...
    {% luckyorange %}
    </head>
    ...
    </html>


.. _luckyorange-configuration:

Configuration
=============

Before you can use the Lucky Orange integration, you must first set your
Site ID.


.. _luckyorange-id:

Setting the Lucky Orange Site ID
--------------------------------

You can find the Lucky Orange Site ID in the "Settings" of your Lucky
Orange account, reachable via the gear icon on the top right corner.
Set :const:`LUCKYORANGE_SITE_ID` in the project :file:`settings.py` file::

    LUCKYORANGE_SITE_ID = 'XXXXXX'

If you do not set a Lucky Orange Site ID, the code will not be rendered.


.. _luckyorange-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`LUCKYORANGE_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

=====================================
Contentsquare -- enterprise digital experience analytics
=====================================

`Contentsquare`_ is an enterprise digital experience analytics platform that provides comprehensive insights into user behavior across web, mobile, and other digital touchpoints.

.. _`Contentsquare`: https://contentsquare.com/


.. contentsquare-installation:

Installation
============

To start using the Contentsquare integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Contentsquare template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags. If you are, skip to
:ref:`contentsquare-configuration`.

The Contentsquare code is inserted into templates using template tags.
Because every page that you want to track must have the tag,
it is useful to add it to your base template.
At the top of the template, load the :mod:`contentsquare` template tag library.
Then insert the :ttag:`contentsquare` tag at the bottom of the head section::

    {% load contentsquare %}
    <html>
    <head>
    ...
    {% contentsquare %}
    </head>
    ...
    </html>


.. _contentsquare-configuration:

Configuration
=============

Before you can use the Contentsquare integration, you must first set your Site ID.


.. _contentsquare-id:

Setting the Contentsquare Site ID
----------------------------------

You can find the Contentsquare Site ID in the "Sites & Organizations" section of your Contentsquare account.
Set :const:`CONTENTSQUARE_SITE_ID` in the project :file:`settings.py` file::

    CONTENTSQUARE_SITE_ID = 'XXXXXXXXX'

If you do not set a Contentsquare Site ID, the tracking code will not be rendered.


.. _contentsquare-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses. By default, if the tags detect that the client
comes from any address in the :const:`CONTENTSQUARE_INTERNAL_IPS`
setting, the tracking code is commented out. It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default). See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


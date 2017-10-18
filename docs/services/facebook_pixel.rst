=======================================
Facebook Pixel -- advertising analytics
=======================================

`Facebook Pixel`_ is Facebook's tool for conversion tracking, optimisation and remarketing.

.. _`Facebook Pixel`: https://developers.facebook.com/docs/facebook-pixel/


.. facebook-pixel-installation:

Installation
============

To start using the Facebook Pixel integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Facebook Pixel template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`facebook-pixel-configuration`.

The Facebook Pixel code is inserted into templates using template tags.
Because every page that you want to track must have the tag,
it is useful to add it to your base template.
At the top of the template, load the :mod:`facebook_pixel` template tag library.
Then insert the :ttag:`facebook_pixel_head` tag at the bottom of the head section,
and optionally insert the :ttag:`facebook_pixel_body` tag at the bottom of the body section::

    {% load facebook_pixel %}
    <html>
    <head>
    ...
    {% facebook_pixel_head %}
    </head>
    <body>
    ...
    {% facebook_pixel_body %}
    </body>
    </html>

.. note::
    The :ttag:`facebook_pixel_body` tag code will only be used for browsers with JavaScript disabled.
    It can be omitted if you don't need to support them.


.. _facebook-pixel-configuration:

Configuration
=============

Before you can use the Facebook Pixel integration,
you must first set your Pixel ID.


.. _facebook-pixel-id:

Setting the Pixel ID
--------------------

Each Facebook Adverts account you have can have a Pixel ID,
and the :mod:`facebook_pixel` tags will include it in the rendered page.
You can find the Pixel ID on the "Pixels" section of your Facebook Adverts account.
Set :const:`FACEBOOK_PIXEL_ID` in the project :file:`settings.py` file::

    FACEBOOK_PIXEL_ID = 'XXXXXXXXXX'

If you do not set a Pixel ID, the code will not be rendered.


.. _facebook-pixel-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`FACEBOOK_PIXEL_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

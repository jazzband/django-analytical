===============================================
 Google Analytics (gtag.js) -- traffic analysis
===============================================

`Google Analytics`_ is the well-known web analytics service from
Google.  The product is aimed more at marketers than webmasters or
technologists, supporting integration with AdWords and other e-commence
features.  The global site tag (`gtag.js`_) is a JavaScript tagging
framework and API that allows you to send event data to Google Analytics,
Google Ads, and Google Marketing Platform.

.. _`Google Analytics`: http://www.google.com/analytics/
.. _`gtag.js`: https://developers.google.com/analytics/devguides/collection/gtagjs/


.. google-analytics-installation:

Installation
============

To start using the Google Analytics integration, you must have installed
the django-analytical package and have added the ``analytical``
application to :const:`INSTALLED_APPS` in your project
:file:`settings.py` file. See :doc:`../install` for details.

Next you need to add the Google Analytics template tag to your
templates. This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`google-analytics-configuration`.

The Google Analytics tracking code is inserted into templates using a
template tag.  Load the :mod:`google_analytics_gtag` template tag library and
insert the :ttag:`google_analytics_gtag` tag.  Because every page that you
want to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the bottom of the HTML head::

    {% load google_analytics_gtag %}
    <html>
    <head>
    {% google_analytics_gtag %}
    ...
    </head>
    ...


.. _google-analytics-configuration:

Configuration
=============

Before you can use the Google Analytics integration, you must first set
your website property ID.  If you track multiple domains with the same
code, you also need to set-up the domain.  Finally, you can add custom
segments for Google Analytics to track.


.. _google-analytics-property-id:

Setting the property ID
-----------------------

Every website you track with Google Analytics gets its own property ID,
and the :ttag:`google_analytics_gtag` tag will include it in the rendered
Javascript code.  You can find the web property ID on the overview page
of your account.  Set :const:`GOOGLE_ANALYTICS_GTAG_PROPERTY_ID` in the
project :file:`settings.py` file::

    GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = 'UA-XXXXXX-X'

If you do not set a property ID, the tracking code will not be rendered.

Please node that the accepted Property IDs should be one of the following formats:

- 'UA-XXXXXX-Y'
- 'AW-XXXXXXXXXX'
- 'G-XXXXXXXX'
- 'DC-XXXXXXXX'


Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`GOOGLE_ANALYTICS_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

.. _google-analytics-identify-user:

Identifying authenticated users
-------------------------------

The username of an authenticated user is passed to Google Analytics
automatically as the `user_id`.  See :ref:`identifying-visitors`.

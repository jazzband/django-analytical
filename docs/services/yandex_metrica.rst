==================================
Yandex.Metrica -- traffic analysis
==================================

`Yandex.Metrica`_ is an analytics tool like as google analytics.

.. _`Yandex.Metrica`: http://metrica.yandex.com/


.. yandex-metrica-installation:

Installation
============

To start using the Yandex.Metrica integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Yandex.Metrica template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`yandex-metrica-configuration`.

The Yandex.Metrica counter code is inserted into templates using a template
tag.  Load the :mod:`yandex_metrica` template tag library and insert the
:ttag:`yandex_metrica` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML head::

    {% load yandex_metrica %}
    <html>
    <head>
    ...
    {% yandex_metrica %}
    </head>
    ...


.. _yandex-metrica-configuration:

Configuration
=============

Before you can use the Yandex.Metrica integration, you must first set
your website counter ID.


.. _yandex-metrica-counter-id:

Setting the counter ID
----------------------

Every website you track with Yandex.Metrica gets its own counter ID,
and the :ttag:`yandex_metrica` tag will include it in the rendered
Javascript code.  You can find the web counter ID on the overview page
of your account.  Set :const:`YANDEX_METRICA_COUNTER_ID` in the
project :file:`settings.py` file::

    YANDEX_METRICA_COUNTER_ID = '12345678'

If you do not set a counter ID, the counter code will not be rendered.

You can set additional options to tune your counter:

============================  =============  =============================================
Constant                      Default Value  Description
============================  =============  =============================================
``YANDEX_METRICA_WEBVISOR``     False        Webvisor, scroll map, form analysis.
``YANDEX_METRICA_TRACKHASH``    False        Hash tracking in the browser address bar.
``YANDEX_METRICA_NOINDEX``      False        Stop automatic page indexing.
``YANDEX_METRICA_ECOMMERCE``    False        Dispatch ecommerce data to Metrica.
============================  =============  =============================================

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`YANDEX_METRICA_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

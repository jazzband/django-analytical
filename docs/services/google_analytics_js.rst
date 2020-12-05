====================================================
 Google Analytics (analytics.js) -- traffic analysis
====================================================

`Google Analytics`_ is the well-known web analytics service from
Google.  The product is aimed more at marketers than webmasters or
technologists, supporting integration with AdWords and other e-commence
features.  The `analytics.js`_ library (also known as "the Google
Analytics tag") is a JavaScript library for measuring how users interact
with your website.

.. _`Google Analytics`: http://www.google.com/analytics/
.. _`analytics.js`: https://developers.google.com/analytics/devguides/collection/analyticsjs/


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
template tag.  Load the :mod:`google_analytics_js` template tag library and
insert the :ttag:`google_analytics_js` tag.  Because every page that you
want to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the bottom of the HTML head::

    {% load google_analytics_js %}
    <html>
    <head>
    ...
    {% google_analytics_js %}
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
and the :ttag:`google_analytics_js` tag will include it in the rendered
Javascript code.  You can find the web property ID on the overview page
of your account.  Set :const:`GOOGLE_ANALYTICS_JS_PROPERTY_ID` in the
project :file:`settings.py` file::

    GOOGLE_ANALYTICS_JS_PROPERTY_ID = 'UA-XXXXXXXX-X'

If you do not set a property ID, the tracking code will not be rendered.


Tracking multiple domains
-------------------------

The default code is suitable for tracking a single domain.  If you track
multiple domains, set the :const:`GOOGLE_ANALYTICS_TRACKING_STYLE`
setting to one of the :const:`analytical.templatetags.google_analytics_js.TRACK_*`
constants:

=============================  =====  =============================================
Constant                       Value  Description
=============================  =====  =============================================
``TRACK_SINGLE_DOMAIN``          1    Track one domain.
``TRACK_MULTIPLE_SUBDOMAINS``    2    Track multiple subdomains of the same top
                                      domain (e.g. `fr.example.com` and
                                      `nl.example.com`).
``TRACK_MULTIPLE_DOMAINS``       3    Track multiple top domains (e.g. `example.fr`
                                      and `example.nl`).
=============================  =====  =============================================

As noted, the default tracking style is
:const:`~analytical.templatetags.google_analytics_js.TRACK_SINGLE_DOMAIN`.

When you track multiple (sub)domains, django-analytical needs to know
what domain name to pass to Google Analytics.  If you use the contrib
sites app, the domain is automatically picked up from the current
:const:`~django.contrib.sites.models.Site` instance.  Otherwise, you may
either pass the domain to the template tag through the context variable
:const:`google_analytics_domain` (fallback: :const:`analytical_domain`)
or set it in the project :file:`settings.py` file using
:const:`GOOGLE_ANALYTICS_DOMAIN` (fallback: :const:`ANALYTICAL_DOMAIN`).

Display Advertising
-------------------

Display Advertising allows you to view Demographics and Interests reports,
add Remarketing Lists and support DoubleClick Campain Manager integration.

You can enable `Display Advertising features`_ by setting the
:const:`GOOGLE_ANALYTICS_DISPLAY_ADVERTISING` configuration setting::

    GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True

By default, display advertising features are disabled.

.. _`Display Advertising features`: https://support.google.com/analytics/answer/3450482


.. _google-analytics-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`GOOGLE_ANALYTICS_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _google-analytics-custom-variables:

Custom variables
----------------

As described in the Google Analytics `custom variables`_ documentation
page, you can define custom segments.  Using template context variables
``google_analytics_var1`` through ``google_analytics_var5``, you can let
the :ttag:`google_analytics_js` tag pass custom variables to Google
Analytics automatically.  You can set the context variables in your view
when your render a template containing the tracking code::

    context = RequestContext({'google_analytics_var1': ('gender', 'female'),
                              'google_analytics_var2': ('visit', 1)})
    return some_template.render(context)

The value of the context variable is a tuple *(name, value)*.

You may want to set custom variables in a context processor that you add
to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def google_analytics_segment_language(request):
        try:
            return {'google_analytics_var3': request.LANGUAGE_CODE}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

.. _`custom variables`: https://developers.google.com/analytics/devguides/collection/upgrade/reference/gajs-analyticsjs#custom-vars


.. _google-analytics-anonimyze-ips:

Anonymize IPs
-------------

You can enable the `IP anonymization`_ feature by setting the
:const:`GOOGLE_ANALYTICS_ANONYMIZE_IP` configuration setting::

    GOOGLE_ANALYTICS_ANONYMIZE_IP = True

This may be mandatory for deployments in countries that have a firm policies
concerning data privacy (e.g. Germany).

By default, IPs are not anonymized.

.. _`IP anonymization`: https://support.google.com/analytics/bin/answer.py?hl=en&answer=2763052


.. _google-analytics-sample-rate:

Sample Rate
-----------

You can configure the `Sample Rate`_ feature by setting the
:const:`GOOGLE_ANALYTICS_SAMPLE_RATE` configuration setting::

    GOOGLE_ANALYTICS_SAMPLE_RATE = 10

The value is a percentage and can be between 0 and 100 and can be a string or
integer value.

.. _`Sample Rate`: https://developers.google.com/analytics/devguides/collection/analyticsjs/field-reference#sampleRate


.. _google-analytics-site-speed-sample-rate:

Site Speed Sample Rate
----------------------

You can configure the `Site Speed Sample Rate`_ feature by setting the
:const:`GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE` configuration setting::

    GOOGLE_ANALYTICS_SITE_SPEED_SAMPLE_RATE = 10

The value is a percentage and can be between 0 and 100 and can be a string or
integer value.

.. _`Site Speed Sample Rate`: https://developers.google.com/analytics/devguides/collection/analyticsjs/field-reference#siteSpeedSampleRate


.. _google-analytics-cookie-expiration:

Cookie Expiration
----------------------

You can configure the `Cookie Expiration`_ feature by setting the
:const:`GOOGLE_ANALYTICS_COOKIE_EXPIRATION` configuration setting::

    GOOGLE_ANALYTICS_COOKIE_EXPIRATION = 3600000

The value is the cookie expiration in seconds or 0 to delete the cookie when the browser is closed.

.. _`Cookie Expiration`: https://developers.google.com/analytics/devguides/collection/gajs/methods/gaJSApiBasicConfiguration#_setsessioncookietimeout

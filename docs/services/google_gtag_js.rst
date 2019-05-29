======================================
 Google Analytics (gtag.js) -- traffic analysis
======================================

`Google Analytics`_ is the well-known web analytics service from
Google.  The product is aimed more at marketers than webmasters or
technologists, supporting integration with AdWords and other e-commence
features.
This uses the gtags.js version of google analytics.

.. _`Google Analytics`: https://developers.google.com/analytics/


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
template tag.  Load the :mod:`google_gtag_js` template tag library and
insert the :ttag:`google_gtag_js` tag.  Because every page that you
want to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the top of the HTML head::

    {% load google_gtag_js %}
    <html>
    <head>
    {% google_gtag_js %}
    ...

    </head>
    ...


.. _google-analytics-configuration:

Configuration
=============

Before you can use the Google Analytics integration, you must first set
your website property ID. Then you can set any analytics config variables
you wish Google Analytics to track.


.. _google-analytics-property-id:

Setting the property ID
-----------------------

Every website you track with Google Analytics gets its own property ID,
and the :ttag:`google_gtag_js` tag will include it in the rendered
Javascript code.  You can find the web property ID on the overview page
of your account.  Set :const:`GOOGLE_GTAG_JS_PROPERTY_ID` in the
project :file:`settings.py` file::

    GOOGLE_GTAG_JS_PROPERTY_ID = 'UA-XXXXXX-X'

If you do not set a property ID, the tracking code will not be rendered.


Google Analytics Tracking Config
---------------------

:ttag:`google_gtag_js` works by letting you use gtag.js 's
'set' and 'config' `javascript commands
<https://developers.google.com/gtagjs/reference/api>`_
.  
The 'set' gtag commands are inserted before the 'config' commands.  

You are given the option to 'set' gtag values for a request
via context variable ``google_gtag_js_set_data``. If used, this should be
a json serializable object, to be used like ``gtag('set', <value>)``.

Additionally, you can use ``google_gtag_js_set1`` though
``google_gtag_js_set5``, which should each be key value pairs, to be
used like ``gtag('set', <key>, <value>)``.  
Key should be a string, and value a json serializable object (which includes strings).


At the present, :ttag:`google_gtag_js` only supports
configuring one 'GA_MEASUREMENT_ID' property.  
The options for this config can be set in the following ways:

1. Via setting: :const:`GOOGLE_GTAG_JS_DEFAULT_CONFIG` - which should
   be a json serializable dictionary of all default config
   options. This value will be used as the default config on all pages.
2. Via the context variable ``google_gtag_js_config_data``, again a
   json serializable dictionary.  
   The resultant config options will be made from the default config
   updated with the values of this 'per request' config.

Note re config options:
Provided you find the right key name, you should be able to configure
the gtag tracking however you need it.  
You can use :file:`settings.py` options such as::

    GOOGLE_GTAG_JS_DEFAULT_CONFIG = {
        'anonymize_ip': True,
        'send_page_view': False,
        'custom_map': {
            'dimension<Index>': 'dimension_name',
        },
    }



You may also like to create a context processor for setting the gtag
'set' and 'config' options per request, that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`, eg::

    def process_google_gtag_options(request):
        google_gtag_options = {}
        google_gtag_options['google_gtag_js_set1'] = ('dimension1', request.some_data)
        google_gtag_options['google_gtag_js_config_data'] = {
            'currency': 'USD',
            'country': 'US',
            'custom_map': {'metric5': 'avg_page_load_time'},
        }
        return google_gtag_options



Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`GOOGLE_ANALYTICS_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.



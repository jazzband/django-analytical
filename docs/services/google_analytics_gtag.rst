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
:ref:`google-analytics-configuration-gtag`.

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


.. _google-analytics-configuration-gtag:

Configuration
=============

Before you can use the Google Analytics integration, you must first set
your website property ID.  If you track multiple domains with the same
code, you also need to set-up the domain.  Finally, you can add custom
segments for Google Analytics to track.


.. _google-analytics-gtag-property-id:

Setting the property ID
-----------------------

Every website you track with Google Analytics gets its own property ID,
and the :ttag:`google_analytics_gtag` tag will include it in the rendered
JavaScript code.  You can find the web property ID on the overview page
of your account.  Set :const:`GOOGLE_ANALYTICS_GTAG_PROPERTY_ID` in the
project :file:`settings.py` file::

    GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = 'UA-XXXXXX-X'

If you do not set a property ID, the tracking code will not be rendered.

Please note that the accepted Property IDs should be one of the following formats:

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
automatically as the ``user_id``.  See :ref:`identifying-visitors`.

According to `Google Analytics conditions`_ you should avoid
sending Personally Identifiable Information.
Using ``username`` as ``user_id`` might not be the best option.
To avoid that, you can change the identity
by setting ``google_analytics_gtag_identity`` (or ``analytical_identity`` to
affect all providers) context variable:

.. code-block:: python

    context = RequestContext({'google_analytics_gtag_identity': user.uuid})
    return some_template.render(context)

or in the template:

.. code-block:: django

    {% with google_analytics_gtag_identity=request.user.uuid|default:None %}
        {% analytical_head_top %}
    {% endwith %}

.. _`Google Analytics conditions`: https://developers.google.com/analytics/solutions/crm-integration#user_id

.. _google-analytics-custom-dimensions:

Custom dimensions
----------------

As described in the Google Analytics `custom dimensions`_ documentation
page, you can define custom dimensions which are variables specific to your
business needs. These variables can include both custom event parameters as
well as customer user properties. Using the template context variable
``google_analytics_custom_dimensions``, you can let the :ttag:`google_analytics_gtag`
pass custom dimensions to Google Analytics automatically. The ``google_analytics_custom_dimensions``
variable must be set to a dictionary where the keys are the dimension names
and the values are the dimension values. You can set the context variable in your
view when you render a template containing the tracking code::

.. code-block:: python

    context = RequestContext({
        'google_analytics_custom_dimensions': {
                'gender': 'female',
                'country': 'US',
                'user_properties': {
                    'age': 25
                }
            }
        })
    return some_template.render(context)

Note that the ``user_properties`` key is used to pass user properties to Google
Analytics. It's not necessary to always use this key, but that'd be the way of
sending user properties to Google Analytics automatically.

You may want to set custom dimensions in a context processor that you add
to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

.. code-block:: python

    def google_analytics_segment_language(request):
        try:
            return {'google_analytics_custom_dimensions': {'language': request.LANGUAGE_CODE}}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

.. _`custom dimensions`: https://support.google.com/analytics/answer/10075209

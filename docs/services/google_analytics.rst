====================================
Google Analytics -- traffic analysis
====================================

`Google Analytics`_ is the well-known web analytics service from
Google.  The product is aimed more at marketers than webmasters or
technologists, supporting integration with AdWords and other e-commence
features.

.. _`Google Analytics`: http://www.google.com/analytics/


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
template tag.  Load the :mod:`google_analytics` template tag library and
insert the :ttag:`google_analytics` tag.  Because every page that you
want to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the bottom of the HTML head::

    {% load google_analytics %}
    <html>
    <head>
    ...
    {% google_analytics %}
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
and the :ttag:`google_analytics` tag will include it in the rendered
Javascript code.  You can find the web property ID on the overview page
of your account.  Set :const:`GOOGLE_ANALYTICS_PROPERTY_ID` in the
project :file:`settings.py` file::

    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-XXXXXX-X'

If you do not set a property ID, the tracking code will not be rendered.


Tracking multiple domains
-------------------------

The default code is suitable for tracking a single domain.  If you track
multiple domains, set the :const:`GOOGLE_ANALYTICS_TRACKING_STYLE`
setting to one of the :const:`analytical.google_analytics.SCOPE_*`
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
:const:`~analytical.google_analytics.TRACK_SINGLE_DOMAIN`.

When you track multiple (sub)domains, django-analytical needs to know
what domain name to pass to Google Analytics.  If you use the contrib
sites app, the domain is automatically picked up from the current
:const:`~django.contrib.sites.models.Site` instance.  Otherwise, you may
either pass the domain to the template tag through the context variable
:const:`google_analytics_domain` (fallback: :const:`analytical_domain`)
or set it in the project :file:`settings.py` file using
:const:`GOOGLE_ANALYTICS_DOMAIN` (fallback: :const:`ANALYTICAL_DOMAIN`).


Tracking site speed
-------------------

You can view page load times in the `Site Speed report`_ by setting the
:const:`GOOGLE_ANALYTICS_SITE_SPEED` configuration setting::

    GOOGLE_ANALYTICS_SITE_SPEED = True

By default, page load times are not tracked.

.. _`Site Speed report`: http://www.google.com/support/analyticshelp/bin/answer.py?answer=1205784&topic=1282106


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
the :ttag:`google_analytics` tag pass custom variables to Google
Analytics automatically.  You can set the context variables in your view
when your render a template containing the tracking code::

    context = RequestContext({'google_analytics_var1': ('gender', 'female'),
                              'google_analytics_var2': ('visit', '1', SCOPE_SESSION)})
    return some_template.render(context)

The value of the context variable is a tuple *(name, value, [scope])*.
The scope parameter is one of the
:const:`analytical.google_analytics.SCOPE_*` constants:

=================  ======  =============================================
Constant           Value   Description
=================  ======  =============================================
``SCOPE_VISITOR``    1     Distinguishes categories of visitors across
                           multiple sessions.
``SCOPE_SESSION``    2     Ddistinguishes different visitor experiences
                           across sessions.
``SCOPE_PAGE``       3     Defines page-level activity.
=================  ======  =============================================

The default scope is :const:`~analytical.google_analytics.SCOPE_PAGE`.

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

.. _`custom variables`: http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html

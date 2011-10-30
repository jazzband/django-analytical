=====================================
Spring Metrics -- conversion tracking
=====================================

`Spring Metrics`_ is a convesions analysis tool.  It shows you the top
converting sources, search keywords ande landing pages.  The real-time
dashboard shows you how customers interacted with your website and how
to increase conversion.

.. _`Spring Metrics`: http://www.springmetrics.com/


Installation
============

To start using the Spring Metrics integration, you must have installed
the django-analytical package and have added the ``analytical``
application to :const:`INSTALLED_APPS` in your project
:file:`settings.py` file.  See :doc:`../install` for details.

Next you need to add the Spring Metrics template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`spring-metrics-configuration`.

The Spring Metrics tracking code is inserted into templates using a
template tag.  Load the :mod:`spring_metrics` template tag library and
insert the :ttag:`spring_metrics` tag.  Because every page that you
want to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the bottom of the HTML head::

    {% load spring_metrics %}
    <html>
    <head>
    ...
    {% spring_metrics %}
    </head>
    ...


.. _spring-metrics-configuration:

Configuration
=============

Before you can use the Spring Metrics integration, you must first set
your website Tracking ID.  You can also customize the data that Spring
Metrics tracks.


Setting the Tracking ID
-----------------------

Every website you track with Spring Metrics gets its own Tracking ID,
and the :ttag:`spring_metrics` tag will include it in the rendered
Javascript code.  You can find the Tracking ID in the `manage page`_
of your Spring Metrics account.  Set :const:`SPRING_METRICS_TRACKING_ID`
in the project :file:`settings.py` file::

    SPRING_METRICS_TRACKING_ID = 'XXXXXXXXXX'

If you do not set a Tracking ID, the tracking code will not be rendered.

.. _`manage page`: https://app.springmetrics.com/manage/


Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`SPRING_METRICS_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


Tracking revenue
----------------

The most important value tracked by Spring Metrics is that of revenue.
Using the :data:`spring_metrics_revenue` template context variable, you
can let the :ttag:`spring_metrics` tag pass earned revenue to Spring
Metrics.  You can set the context variable in your view when you render
a template containing thetracking code::

    context = RequestContext({'spring_metrics_revenue': '30.53'})
    return some_template.render(context)


Custom data
-----------

Spring Metrics can also track other data.  Interesting examples would be
transaction IDs or e-mail addresses from logged in users.  By setting
any :data:`spring_metrics_X` template context variable, Spring Metrics
will track a variable named :data:`X`.  For example::

    context = RequestContext({
        'spring_metrics_revenue': '30.53',
        'spring_metrics_order_id': '15445',
    })
    return some_template.render(context)

Some variables should be passed on every page and can be computed from
the request object.  In such cases you will want to set custom
variables in a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def spring_metrics_global_variables(request):
        try:
            profile = request.user.get_profile()
            return {'spring_metrics_city': profile.address.city}
        except (AttributeError, ObjectDoesNotExist):
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.


Identifying authenticated users
-------------------------------

If you have not set the :data:`spring_metrics_email` property
explicitly, the e-mail address of an authenticated user is passed to
Spring Metrics automatically.  See :ref:`identifying-visitors`.


----

Thanks go to Spring Metrics for their support with the development of
this application.

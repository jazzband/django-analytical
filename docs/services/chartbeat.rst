=============================
Chartbeat -- traffic analysis
=============================

Chartbeat_ provides real-time analytics to websites and blogs.  It shows
visitors, load times, and referring sites on a minute-by-minute basis.
The service also provides alerts the second your website crashes or
slows to a crawl.

.. _Chartbeat: http://www.chartbeat.com/


.. chartbeat-installation:

Installation
============

To start using the Chartbeat integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Chartbeat template tags to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`chartbeat-configuration`.

The Chartbeat tracking code is inserted into templates using template
tags.  At the top of the template, load the :mod:`chartbeat` template
tag library.  Then insert the :ttag:`chartbeat_top` tag at the top of
the head section, and the :ttag:`chartbeat_bottom` tag at the bottom of
the body section::

    {% load chartbeat %}
    <html>
    <head>
    {% chartbeat_top %}

    ...

    {% chartbeat_bottom %}
    </body>
    </html>

Because these tags are used to measure page loading time, it is
important to place them as close as possible to the start and end of the
document.


.. _chartbeat-configuration:

Configuration
=============

Before you can use the Chartbeat integration, you must first set your
User ID.


.. _chartbeat-user-id:

Setting the User ID
-------------------

Your Chartbeat account has a unique User ID.  You can find your User ID
by visiting the Chartbeat `Add New Site`_ page.  The second code snippet
contains a line that looks like this::

    var _sf_async_config={uid:XXXXX,domain:"YYYYYYYYYY"};

Here, ``XXXXX`` is your User ID.  Set :const:`CHARTBEAT_USER_ID` in the
project :file:`settings.py` file::

    CHARTBEAT_SITE_ID = 'XXXXX'

If you do not set a User ID, the tracking code will not be rendered.

.. _`Add New Site`: http://chartbeat.com/code/


.. _chartbeat-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`CHARTBEAT_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _chartbeat-domain:

Setting the domain
------------------

The Javascript tracking code can send the website domain to Chartbeat.
If you use multiple subdomains this enables you to treat them as one
website in Chartbeat.  If your project uses the sites framework, the
domain name of the current :class:`~django.contrib.sites.models.Site`
will be passed to Chartbeat automatically.  You can modify this behavior
using the :const:`CHARTBEAT_AUTO_DOMAIN` setting::

    CHARTBEAT_AUTO_DOMAIN = False

Alternatively, you set the domain through the ``chartbeat_domain``
context variable when you render the template::

    context = RequestContext({'chartbeat_domain': 'example.com'})
    return some_template.render(context)

It is annoying to do this for every view, so you may want to set it in
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def chartbeat(request):
        return {'chartbeat_domain': 'example.com'}

The context domain overrides the domain from the current site.  If no
domain is set, either explicitly or implicitly through the sites
framework, then no domain is sent, and Chartbeat will detect the domain
name from the URL.  If your website uses just one domain, this will work
just fine.


----

Thanks go to Chartbeat for their support with the development of this
application.

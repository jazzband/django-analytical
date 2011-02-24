.. _tutorial:

========
Tutorial
========

This tutorial will show you how to install and configure
django-analytical for basic tracking, and then briefly touch on two
common customization issues: visitor identification and custom data
tracking.

Suppose your Django website provides information about the IPv4 to IPv6
transition.  Visitors can discuss their problems and help each other
make the necessary changes to their network infrastructure.  You want to
use two different analytics services:

* :doc:`Clicky <services/clicky>` for detailed traffic analysis
* :doc:`Crazy Egg <services/crazy_egg>` to see where visitors click on
  your pages

At the end of this tutorial, the project will track visitors on both
Clicky and Crazy Egg, identify authenticated users and add extra
tracking data to segment mouse clicks on Crazy Egg based on whether
visitors are using IPv4 or IPv6.


Setting up basic tracking
=========================

To get started with django-analytical, the package must first be
installed.  You can download and install the latest stable package from
the Python Package Index automatically by using ``easy_install``::

    $ easy_install django-analytical

For more ways to install django-analytical, see
:ref:`installing-the-package`.

After you install django-analytical, you need to add it to the list of
installed applications in the ``settings.py`` file of your project::

    INSTALLED_APPS = [
        ...
        'analytical',
        ...
    ]

Then you have to add the general-purpose django-analytical template tags
to your base template::

    {% load analytical %}
    <!DOCTYPE ... >
    <html>
        <head>
            {% analytical_head_top %}

            ...

            {% analytical_head_bottom %}
        </head>
        <body>
            {% analytical_body_top %}

            ...

            {% analytical_body_bottom %}
        </body>
    </html>

Finally, you need to configure the Clicky Site ID and the Crazy Egg
account number.  Add the following to your project :file:`settings.py`
file (replacing the ``x``'s with your own codes)::

    CLICKY_SITE_ID = 'xxxxxxxx'
    CRAZY_EGG_ACCOUNT_NUMBER = 'xxxxxxxx'

The analytics services are now installed.  If you run Django with these
changes, both Clicky and Crazy Egg will be tracking your visitors.


Identifying authenticated users
===============================

Suppose that when your visitors post questions on IPv6 or tell others
about their experience with the transition, they first log in through
the standard Django authentication system.  Clicky can identify and
track individual visitors and you want to use this feature.

If django-analytical template tags detect that the current user is
authenticated, they will automatically include code to send the username
to services that support this feature.  This only works if the template
context has the current user in the ``user`` or ``request.user`` context
variable.  If you use a :class:`~django.template.RequestContext` to
render templates (which is recommended anyway) and have the
:class:`django.contrib.auth.context_processors.auth` context processor
in the :data:`TEMPLATE_CONTEXT_PROCESSORS` setting (which is default),
then this identification works without having to make any changes.

For more detailed information on automatic identification, and how to
disable or override it, see :ref:`identifying-visitors`.


Adding custom tracking data
===========================

Suppose that you think that visitors who already have IPv6 use the
website in a different way from those still on IPv4.  You want to test
this hypothesis by segmenting the Crazy Egg heatmaps based on the IP
protocol version.

In order to filter on protocol version in Crazy Egg, you need to
include the visitor IP protocol version in the Crazy Egg tracking code.
The easiest way to do this is by using a context processor::

    def track_ip_proto(request):
        addr = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if not addr:
            addr = request.META.get('REMOTE_ADDR', '')
        if ':' in addr:
            proto = 'ipv6'
        else:
            proto = 'ipv4'  # assume IPv4 if no information
        return {'crazy_egg_var1': proto}

Use a :class:`~django.template.RequestContext` when rendering templates
and add the ``'track_ip_proto'`` to :data:`TEMPLATE_CONTEXT_PROCESSORS`.
In Crazy Egg, you can now select *User Var1* in the overlay or confetti
views to see whether visitors using IPv4 behave differently from those
using IPv6.


----

This concludes the tutorial.  For information about setting up,
configuring and customizing the different analytics services, see
:doc:`features` and :doc:`services`.

=========================
Optimizely -- A/B testing
=========================

Optimizely_ is an easy way to implement A/B testing.  Try different
decisions, images, layouts, and copy without touching your website code
and see exactly how your experiments are affecting pageviews,
retention and sales.

.. _Optimizely: http://www.optimizely.com/


.. optimizely-installation:

Installation
============

To start using the Optimizely integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Optimizely template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`optimizely-configuration`.

The Optimizely Javascript code is inserted into templates using a
template tag.  Load the :mod:`optimizely` template tag library and
insert the :ttag:`optimizely` tag.  Because every page that you want to
track must have the tag, it is useful to add it to your base template.
Insert the tag at the top of the HTML head::

    {% load optimizely %}
    <html>
    <head>
    {% optimizely %}
    ...


.. _optimizely-configuration:

Configuration
=============

Before you can use the Optimizely integration, you must first set your
account number.


.. _optimizely-account-number:

Setting the account number
--------------------------

Optimizely gives you a unique account number, and the :ttag:`optimizely`
tag will include it in the rendered Javascript code.  You can find your
account number by clicking the *Implementation* link in the top
right-hand corner of the Optimizely website.  A pop-up window will
appear containing HTML code looking like this::

    <script src="//cdn.optimizely.com/js/XXXXXXX.js"></script>

The number ``XXXXXXX`` is your account number.  Set
:const:`OPTIMIZELY_ACCOUNT_NUMBER` in the project :file:`settings.py`
file::

    OPTIMIZELY_ACCOUNT_NUMBER = 'XXXXXXX'

If you do not set an account number, the Javascript code will not be
rendered.


.. _optimizely-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`OPTIMIZELY_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

==========================
Clicky -- traffic analysis
==========================

Clicky_ is an online web analytics tool.  It is similar to Google
Analytics in that it provides statistics on who is visiting your website
and what they are doing.  Clicky provides its data in real time and is
designed to be very easy to use.

.. _Clicky: http://getclicky.com/


.. clicky-installation:

Installation
============

To start using the Clicky integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Clicky template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`clicky-configuration`.

The Clicky tracking code is inserted into templates using a template
tag.  Load the :mod:`clicky` template tag library and insert the
:ttag:`clicky` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body::

    {% load clicky %}
    ...
    {% clicky %}
    </body>
    </html>


.. _clicky-configuration:

Configuration
=============

Before you can use the Clicky integration, you must first set your
website Site ID.  You can also customize the data that Clicky tracks.


.. _clicky-site-id:

Setting the Site ID
-------------------

Every website you track with Clicky gets its own Site ID, and the
:ttag:`clicky` tag will include it in the rendered JavaScript code.
You can find the Site ID in the *Info* tab of the website *Preferences*
page, in your Clicky account.  Set :const:`CLICKY_SITE_ID` in the
project :file:`settings.py` file::

    CLICKY_SITE_ID = 'XXXXXXXX'

If you do not set a Site ID, the tracking code will not be rendered.


Referrer policy
---------------

Clicky's domain validation requires the browser to send a referrer to its
tracking endpoint. Django's default ``SECURE_REFERRER_POLICY`` has been
``same-origin`` since Django 3.1. Both ``same-origin`` and ``no-referrer``
suppress this cross-origin referrer and prevent domain validation.
When ``CLICKY_SITE_ID`` is configured and Django's ``SecurityMiddleware`` is
enabled, the ``analytical.W001`` security system check warns for these
settings. It runs with ``manage.py check`` (or ``manage.py check --tag security``)
and commands that run Django's checks, such as ``runserver``. Rendering a
Clicky tag does not emit a warning.

If you use Clicky's domain validation, choose a policy that sends the origin
to Clicky, for example::

    SECURE_REFERRER_POLICY = 'origin-when-cross-origin'

This sends only the origin, rather than the full page URL, for cross-origin
requests. Review the policy's effect on your other integrations before
changing it. Also check any ``Referrer-Policy`` header set by your views,
web server, or proxy, as the check can only inspect the Django setting.
The check does not change response headers or verify your Clicky account's
preferences. If you have intentionally disabled Clicky's optional domain
validation, you can silence this check::

    SILENCED_SYSTEM_CHECKS = ['analytical.W001']

System checks are not automatically run by Django's deployment WSGI stack;
run ``manage.py check`` explicitly as part of deployment if needed.
See `Clicky's domain validation documentation
<https://clicky.com/help/faq/tips/different/domain-validation>`_ for details.


.. _clicky-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`CLICKY_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _clicky-custom-data:

Custom data
-----------

As described in the Clicky `customized tracking`_ documentation page,
the data that is tracked by Clicky can be customized by setting the
:data:`clicky_custom` JavaScript variable before loading the tracking
code.  Using template context variables, you can let the :ttag:`clicky`
tag pass custom data to Clicky automatically.  You can set the context
variables in your view when you render a template containing the
tracking code::

    context = RequestContext({'clicky_title': 'A better page title'})
    return some_template.render(context)

It is annoying to do this for every view, so you may want to set custom
properties in a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def clicky_global_properties(request):
        return {'clicky_timeout': 10}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

Here is a table with the most important variables.  All variables listed
on the `customized tracking`_ documentation page can be set by replacing
``clicky_custom.`` with ``clicky_``.

==================  ===============  ===================================
Context variable    Clicky property  Description
==================  ===============  ===================================
``clicky_session``  session_         Session data.  A dictionary
                                     containing ``username`` and/or
                                     ``group`` keys.
------------------  ---------------  -----------------------------------
``clicky_goal``     goal_            A succeeded goal.  A dictionary
                                     containing ``id`` and optionally
                                     ``revenue`` keys.
------------------  ---------------  -----------------------------------
``clicky_split``    split_           Split testing page version.  A
                                     dictionary containing ``name``,
                                     ``version`` and optionally ``goal``
                                     keys.
------------------  ---------------  -----------------------------------
``clicky_href``     href_            The URL as tracked by Clicky.
                                     Default is the page URL.
------------------  ---------------  -----------------------------------
``clicky_title``    title_           The page title as tracked by
                                     Clicky.  Default is the HTML title.
==================  ===============  ===================================

.. _`customized tracking`: http://getclicky.com/help/customization
.. _session: http://getclicky.com/help/customization#session
.. _goal: http://getclicky.com/help/customization#goal
.. _href: http://getclicky.com/help/customization#href
.. _title: http://getclicky.com/help/customization#title
.. _split: http://getclicky.com/help/customization#split


.. _clicky-identify-user:

Identifying authenticated users
-------------------------------

If you have not set the session_ property explicitly, the username of an
authenticated user is passed to Clicky automatically.  See
:ref:`identifying-visitors`.


----

Thanks go to Clicky for their support with the development of this
application.

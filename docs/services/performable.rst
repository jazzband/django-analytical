==============================================
Performable -- web analytics and landing pages
==============================================

Performable_ provides a platform for inbound marketing, landing pages
and web analytics.  Its analytics module tracks individual customer
interaction, funnel and e-commerce analysis.  Landing pages can be
created and designed on-line, and integrated with you existing website.

.. _Performable: http://www.performable.com/


.. performable-installation:

Installation
============

To start using the Performable integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Performable template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`performable-configuration`.

The Performable Javascript code is inserted into templates using a
template tag.  Load the :mod:`performable` template tag library and
insert the :ttag:`performable` tag.  Because every page that you want to
track must have the tag, it is useful to add it to your base template.
Insert the tag at the bottom of the HTML body::

    {% load performable %}
    ...
    {% performable %}
    </body>
    </html>


.. _performable-configuration:

Configuration
=============

Before you can use the Performable integration, you must first set your
API key.


.. _performable-account-code:

Setting the API key
-------------------

You Performable account has its own API key, which :ttag:`performable`
tag will include it in the rendered Javascript code.  You can find your
API key on the *Account Settings* page (click 'Account Settings' in the
top right-hand corner of your Performable dashboard).  Set
:const:`PERFORMABLE_API_KEY` in the project :file:`settings.py` file::

    PERFORMABLE_API_KEY = 'XXXXXX'

If you do not set an API key, the Javascript code will not be rendered.


.. _performable-identity-user:

Identifying authenticated users
-------------------------------

If your websites identifies visitors, you can pass this information on
to Performable so that you can track individual users.  By default, the
username of an authenticated user is passed to Performable
automatically.  See :ref:`identifying-visitors`.

You can also send the visitor identity yourself by adding either the
``performable_identity`` or the ``analytical_identity`` variable to
the template context.  If both variables are set, the former takes
precedence. For example::

    context = RequestContext({'performable_identity': identity})
    return some_template.render(context)

If you can derive the identity from the HTTP request, you can also use
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def identify(request):
        try:
            return {'performable_identity': request.user.email}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.


.. _performable-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`PERFORMABLE_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _performable-embed-page:

Embedding a landing page
========================

You can embed a Performable landing page in your Django website.  The
:ttag:`performable_embed` template tag adds the Javascript code to embed
the page.  It takes two arguments: the hostname and the page ID::

    {% performable_embed HOSTNAME PAGE_ID %}

To find the hostname and page ID, select :menuselection:`Manage -->
Manage Landing Pages` on your Performable dashboard.  Select the landing
page you want to embed.  Look at the URL in your browser address bar; it
will look like this::

    http://my.performable.com/s/HOSTNAME/page/PAGE_ID/

(If you are placing the hostname and page id values in the template, do
not forget to enclose them in quotes or they will be considered context
variable names.)


----

Thanks go to Performable for their support with the development of this
application.

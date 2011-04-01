===============================
GoSquared -- traffic monitoring
===============================

GoSquared_ provides both real-time traffic monitoring and and trends.
It tells you what is currently happening at your website, what is
popular, locate and identify visitors and track twitter.

.. _GoSquared: http://www.gosquared.com/


Installation
============

To start using the GoSquared integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the GoSquared template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`gosquared-configuration`.

The GoSquared tracking code is inserted into templates using a template
tag.  Load the :mod:`gosquared` template tag library and insert the
:ttag:`gosquared` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body::

    {% load gosquared %}
    ...
    {% gosquared %}
    </body>
    </html>


.. _gosquared-configuration:

Configuration
=============

When you set up a website to be tracked by GoSquared, it assigns the
site a token.  You can find the token on the *Tracking Code* tab of your
website settings page.  Set :const:`GOSQUARED_SITE_TOKEN` in the project
:file:`settings.py` file::

    GOSQUARED_SITE_TOKEN = 'XXX-XXXXXX-X'

If you do not set a site token, the tracking code will not be rendered.


Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`GOSQUARED_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


Identifying authenticated users
-------------------------------

If your websites identifies visitors, you can pass this information on
to GoSquared to display on the LiveStats dashboard.  By default, the
name of an authenticated user is passed to GoSquared automatically.  See
:ref:`identifying-visitors`.

You can also send the visitor identity yourself by adding either the
``gosquared_identity`` or the ``analytical_identity`` variable to
the template context.  If both variables are set, the former takes
precedence. For example::

    context = RequestContext({'gosquared_identity': identity})
    return some_template.render(context)

If you can derive the identity from the HTTP request, you can also use
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def identify(request):
        try:
            return {'gosquared_identity': request.user.username}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.


----

Thanks go to GoSquared for their support with the development of this
application.

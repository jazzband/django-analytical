================================
Reinvigorate -- visitor tracking
================================

Reinvigorate_ gives you real-time traffic analysis, visitor activity,
search and referrer information and click heatmaps.  A system tray /
system status bar application for your desktop notifies you when
interesting events occur.

.. _Reinvigorate: http://www.reinvigorate.com/


.. reinvigorate-installation:

Installation
============

To start using the Reinvigorate integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Reinvigorate template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`reinvigorate-configuration`.

The Reinvigorate tracking code is inserted into templates using a
template tag.  Load the :mod:`reinvigorate` template tag library and
insert the :ttag:`reinvigorate` tag.  Because every page that you want
to track must have the tag, it is useful to add it to your base
template.  Insert the tag somewhere within the HTML body::

    {% load reinvigorate %}
    ...
    {% reinvigorate %}
    </body>
    </html>


.. _reinvigorate-configuration:

Configuration
=============

Before you can use the Reinvigorate integration, you must first set your
tracking ID.  You can also customize the data that Reinvigorate tracks.


.. _reinvigorate-tracking-id:

Setting the tracking ID
-----------------------

Every website you track with Reinvigorate gets a tracking ID, and the
:ttag:`reinvigorate` tag will include it in the rendered Javascript
code.  You can find the tracking ID in the URL of your website report
pages.  The URL looks like this:

    \https://report.reinvigorate.net/accounts/XXXXX-XXXXXXXXXX/

Here, ``XXXXX-XXXXXXXXXX`` is the tracking ID.  Set
:const:`REINVIGORATE_TRACKING_ID` in the project :file:`settings.py`
file::

    REINVIGORATE_TRACKING_ID = 'XXXXX-XXXXXXXXXX'

If you do not set a tracking ID, the tracking code will not be rendered.


.. _reinvigorate-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`REINVIGORATE_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _reinvigorate-tags:

Reinvigorate tags
-----------------

As described in the Reinvigorate *NameTags* and *Snoop* pages,
the data that is tracked by Reinvigorate can be customized by adding
*tags* to the Javascript tracking code.  (These should not be confused
with Django template tags.)  Using template context variables, you can
let the :ttag:`reinvigorate` template tag pass reinvigorate tags to
automatically.  You can set the context variables in your view when your
render a template containing the tracking code::

    context = RequestContext({'reinvigorate_purchase': True,
                              'reinvigorate_comment': 'Got discount'})
    return some_template.render(context)

If you have tags that are generated on every page, you may want to set
them in a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def reinvigorate_tags(request):
        try:
            return {'name': request.user.username}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

Here is a table with the most important tags.  All tags listed on the
Reinvigorate pages can be set by replacing ``re_XXX_tag`` with
``reinvigorate_XXX``.

=========================  =============================================
Context variable           Description
=========================  =============================================
``reinvigorate_name``      The visitor name.
-------------------------  ---------------------------------------------
``reinvigorate_context``   Some context information about the visitor,
                           e.g. an e-mail address.
-------------------------  ---------------------------------------------
``reinvigorate_purchase``  A boolean indicating whether the visitor has
                           just made a purchase.  Setting this variable
                           triggers an event in the Snoop notification
                           application.
-------------------------  ---------------------------------------------
``reinvigorate_new_user``  A boolean indicating whether the visitor has
                           just registered as a new user.  Setting this
                           variable triggers an event in the Snoop
                           notification application.
-------------------------  ---------------------------------------------
``reinvigorate_comment``   A comment, which is included in a Snoop
                           event notification.
=========================  =============================================


.. _reinvigorate-identify-user:

Identifying authenticated users
-------------------------------

If you have not set the ``reinvigorate_name`` context variable
explicitly, the full name of an authenticated user is passed to
Reinvigorate automatically.  Similarly, the e-mail address is passed
automatically in the ``context`` tag.  See :ref:`identifying-visitors`.


----

Thanks go to Reinvigorate for their support with the development of this
application.

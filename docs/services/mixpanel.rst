==========================
Mixpanel -- event tracking
==========================

Mixpanel_ tracks events and actions to see what features users are using
the most and how they are trending.  You could use it for real-time
analysis of visitor retention or funnels.

.. _Mixpanel: http://www.mixpanel.com/


.. mixpanel-installation:

Installation
============

To start using the Mixpanel integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Mixpanel template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`mixpanel-configuration`.

The Mixpanel Javascript code is inserted into templates using a
template tag.  Load the :mod:`mixpanel` template tag library and
insert the :ttag:`mixpanel` tag.  Because every page that you want
to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the bottom of the HTML head::

    {% load mixpanel %}
    ...
    {% mixpanel %}
    </head>
    <body>
    ...


.. _mixpanel-configuration:

Configuration
=============

Before you can use the Mixpanel integration, you must first set your
token.


.. _mixpanel-api-key:

Setting the token
-----------------

Every website you track events for with Mixpanel gets its own token,
and the :ttag:`mixpanel` tag will include it in the rendered Javascript
code.  You can find the project token on the Mixpanel *projects* page.
Set :const:`MIXPANEL_API_TOKEN` in the project :file:`settings.py`
file::

    MIXPANEL_API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

If you do not set a token, the tracking code will not be rendered.


.. _mixpanel-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`MIXPANEL_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _mixpanel-identify-user:

Identifying users
-----------------

If your websites identifies visitors, you can pass this information on
to Mixpanel so that you can tie events to users.  By default, the
username of an authenticated user is passed to Mixpanel automatically.
See :ref:`identifying-visitors`.

You can also send the visitor identity yourself by adding either the
``mixpanel_identity`` or the ``analytical_identity`` variable to the
template context.  If both variables are set, the former takes
precedence. For example::

    context = RequestContext({'mixpanel_identity': identity})
    return some_template.render(context)

If you can derive the identity from the HTTP request, you can also use
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def identify(request):
        try:
            return {'mixpanel_identity': request.user.email}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.


.. mixpanel-events:

Tracking events
===============

The django-analytical app integrates the Mixpanel Javascript API in
templates.  To tracking events in views or other parts of Django, you
can use Wes Winham's `django-celery`_ package.

If you want to track an event in Javascript, use the asynchronous
notation, as described in the section titled
`"Asynchronous Tracking with Javascript"`_ in the Mixpanel
documentation. For example::

    mpq.push(["track", "play-game", {"level": "12", "weapon": "sword", "character": "knight"}]);

.. _django-celery: http://github.com/winhamwr/mixpanel-celery
.. _`"Asynchronous Tracking with Javascript"`: http://mixpanel.com/api/docs/guides/integration/js#async


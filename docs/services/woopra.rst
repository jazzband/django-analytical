===========================
Woopra -- website analytics
===========================

Woopra_ generates live detailed statistics about the visitors to your
website.  You can watch your visitors navigate live and interact with
them via chat.  The service features notifications, campaigns, funnels
and more.

.. _Woopra: http://www.woopra.com/


Installation
============

To start using the Woopra integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Woopra template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`woopra-configuration`.

The Woopra tracking code is inserted into templates using a template
tag.  Load the :mod:`woopra` template tag library and insert the
:ttag:`woopra` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML head::

    {% load woopra %}
    <html>
    <head>
    ...
    {% woopra %}
    </head>
    ...

Because Javascript code is asynchronous, putting the tag in the head
section increases the chances that a page view is going to be tracked
before the visitor leaves the page.  See for details the `Asynchronous
JavaScript Developer’s Guide`_ on the Woopra website.

.. _`Asynchronous JavaScript Developer’s Guide`: http://www.woopra.com/docs/async/



.. _woopra-configuration:

Configuration
=============

Before you can use the Woopra integration, you must first set the
website domain.  You can also customize the data that Woopra tracks and
identify authenticated users.


Setting the domain
------------------

A Woopra account is tied to a website domain.  Set
:const:`WOOPRA_DOMAIN` in the project :file:`settings.py` file::

    WOOPRA_DOMAIN = 'XXXXXXXX.XXX'

If you do not set a domain, the tracking code will not be rendered.

(In theory, the django-analytical application could get the website
domain from the current ``Site`` or the ``request`` object, but this
setting also works as a sign that the Woopra integration should be
enabled for the :ttag:`analytical.*` template tags.)


Visitor timeout
---------------

The default Woopra visitor timeout -- the time after which Woopra
ignores inactive visitors on a website -- is set at 4 minutes.  This
means that if a user opens your Web page and then leaves it open in
another browser window, Woopra will report that the visitor has gone
away after 4 minutes of inactivity on that page (no page scrolling,
clicking or other action).

If you would like to increase or decrease the idle timeout setting you
can set :const:`WOOPRA_IDLE_TIMEOUT` to a time in milliseconds.  For
example, to set the default timout to 10 minutes::

    WOOPRA_IDLE_TIMEOUT = 10 * 60 * 1000

Keep in mind that increasing this number will not only show you more
visitors on your site at a time, but will also skew your average time on
a page reporting.  So it’s important to keep the number reasonable in
order to accurately make predictions.


Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`WOOPRA_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


Custom data
-----------

As described in the Woopra documentation on `custom visitor data`_,
the data that is tracked by Woopra can be customized.  Using template
context variables, you can let the :ttag:`woopra` tag pass custom data
to Woopra automatically.  You can set the context variables in your view
when your render a template containing the tracking code::

    context = RequestContext({'woopra_cart_value': cart.total_price})
    return some_template.render(context)

For some data, it is annoying to do this for every view, so you may want
to set variables in a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    from django.utils.hashcompat import md5_constructor as md5

    GRAVATAR_URL = 'http://www.gravatar.com/avatar/'

    def woopra_custom_data(request):
        try:
            email = request.user.email
        except AttributeError:
            return {}
        email_hash = md5(email).hexdigest()
        avatar_url = "%s%s" % (GRAVATAR_URL, email_hash)
        return {'woopra_avatar': avatar_url}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

Standard variables that will be displayed in the Woopra live visitor
data are listed in the table below, but you can define any ``woopra_*``
variable you like and have that detail passed from within the visitor
live stream data when viewing Woopra.

====================  ===================================
Context variable       Description
====================  ===================================
``woopra_name``       The visitor's full name.
--------------------  -----------------------------------
``woopra_email``      The visitor's email address.
--------------------  -----------------------------------
``woopra_avatar``     A URL link to a visitor avatar.
====================  ===================================


.. _`custom visitor data`: http://www.woopra.com/docs/tracking/custom-visitor-data/


Identifying authenticated users
-------------------------------

If you have not set the ``woopra_name`` or ``woopra_email`` variables
explicitly, the username and email address of an authenticated user are
passed to Woopra automatically.  See :ref:`identifying-visitors`.


----

Thanks go to Woopra for their support with the development of this
application.

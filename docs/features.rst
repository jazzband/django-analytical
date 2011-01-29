==========================
Features and customization
==========================

The django-analytical application sets up basic tracking without any
further configuration.  This page describes extra features and ways in
which behavior can be customized.


.. _internal-ips:

Internal IP addresses
=====================

Visits by the website developers or internal users are usually not
interesting.  The django-analytical will comment out the service
initialization code if the client IP address is detected as one from the
:data:`ANALYTICAL_INTERNAL_IPS` setting.  The default value for this
setting is :data:`INTERNAL_IPS`.

Example::

    ANALYTICAL_INTERNAL_IPS = ['192.168.1.45', '192.168.1.57']

.. note::

    The template tags can only access the visitor IP address if the
    HTTP request is present in the template context as the
    ``request`` variable.  For this reason, the
    :data:`ANALYTICAL_INTERNAL_IPS` setting only works if you add this
    variable to the context yourself when you render the template, or
    you use the ``RequestContext`` and add
    ``'django.core.context_processors.request'`` to the list of
    context processors in the ``TEMPLATE_CONTEXT_PROCESSORS``
    setting.


.. _identifying-visitors:

Identifying authenticated users
===============================

Some analytics services can track individual users.  If the visitor is
logged in through the standard Django authentication system and the
current user is accessible in the template context, the username can be
passed to the analytics services that support identifying users.  This
feature is configured by the :data:`ANALYTICAL_AUTO_IDENTIFY` setting
and is enabled by default. To disable::

    ANALYTICAL_AUTO_IDENTIFY = False

.. note::

    The template tags can only access the visitor username if the
    Django user is present in the template context either as the
    ``user`` variable, or as an attribute on the HTTP request in the
    ``request`` variable.  Use a
    :class:`~django.template.RequestContext` to render your
    templates and add
    ``'django.contrib.auth.context_processors.auth'`` or
    ``'django.core.context_processors.request'`` to the list of
    context processors in the :data:`TEMPLATE_CONTEXT_PROCESSORS`
    setting.  (The first of these is added by default.)
    Alternatively, add one of the variables to the context yourself
    when you render the template.


.. _identifying-visitors:

========
Settings
========

Here's a full list of all available settings, in alphabetical order, and
their default values.



.. data:: ANALYTICAL_AUTO_IDENTIFY

	Default: ``True``

	Automatically identify logged in users by their username.

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


.. data:: ANALYTICAL_INTERNAL_IPS

	Default: :data:`INTERNAL_IPS`

	A list or tuple of internal IP addresses.  	Tracking code will be
	commented out for visitors from any of these addresses.

	Example::

		ANALYTICAL_INTERNAL_IPS = ['192.168.1.45', '192.168.1.57']

	.. note::

	    The template tags can only access the visitor IP address if the
	    HTTP request is present in the template context as the
	    ``request`` variable.  For this reason, the
	    :data:`ANALYTICAL_INTERNAL_IPS` settings only works if you add
	    this variable to the context yourself when you render the
	    template, or you use the ``RequestContext`` and add
	    ``'django.core.context_processors.request'`` to the list of
	    context processors in the ``TEMPLATE_CONTEXT_PROCESSORS``
	    setting.

==============================
Installation and configuration
==============================

Integration of your analytics service is very simple.  There are four
steps: installing the package, adding it to the list of installed Django
applications, adding the template tags to your base template, and adding
the identifiers for the services you use to the project settings.

#. `Installing the Python package`_
#. `Installing the Django application`_
#. `Adding the template tags to the base template`_
#. `Configuring the application`_


Installing the Python package
=============================

To install django-analytical the ``analytical`` package must be added to
the Python path.  You can install it directly from PyPI using
``easy_install``::

	$ easy_install django-analytical

You can also install directly from source.  Download either the latest
stable version from PyPI_ or any release from GitHub_, or use Git to
get the development code::

	$ git clone https://github.com/jcassee/django-analytical.git

.. _PyPI: http://pypi.python.org/pypi/django-analytical/
.. _GitHub: http://github.com/jcassee/django-analytical

Then install by running the setup script::

	$ cd django-analytical
	$ python setup.py install


Installing the Django application
=================================

After you install django-analytical, add the ``analytical`` Django
application to the list of installed applications in the ``settings.py``
file of your project::

	INSTALLED_APPS = [
		...
		'analytical',
		...
	]


Adding the template tags to the base template
=============================================

Because every analytics service has uses own specific Javascript code
that should be added to the top or bottom of either the head or body
of every HTML page, the django-analytical provides four general-purpose
tags that will render the code needed for the services you are using.
Your base template should look like this::

	{% load analytical %}
	<!DOCTYPE ... >
	<html>
		<head>
			{% analytical_setup_head_top %}

			...

			{% analytical_setup_head_bottom %}
		</head>
		<body>
			{% analytical_setup_body_top %}

			...

			{% analytical_setup_body_bottom %}
		</body>
	</html>


Configuring the application
===========================

Without configuration, the template tags all render the empty string.
You must enable at least one service, and optionally configure other
django-analytical features.


Enabling services
-----------------

By default, only configured analytics services are installed by the
template tags.  You can also use the :data:`ANALYTICAL_SERVICES` setting
to specify the used services explicitly.  Services are configured in the
project ``settings.py`` file.  The settings required to enable each
service are listed here.  See the service documentation for details.

* :doc:`Clicky <services/clicky>`::

	CLICKY_SITE_ID = '12345678'

* :doc:`Crazy Egg <services/crazy_egg>`::

	CRAZY_EGG_ACCOUNT_NUMBER = '12345678'

* :doc:`Google Analytics <services/google_analytics>`::

	GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-1234567-8'

* :doc:`KISSinsights <services/kiss_insights>`::

	KISS_INSIGHTS_ACCOUNT_NUMBER = '12345'
	KISS_INSIGHTS_SITE_CODE = 'abc'

* :doc:`KISSmetrics <services/kiss_metrics>`::

	KISS_METRICS_API_KEY = '0123456789abcdef0123456789abcdef01234567'

* :doc:`Mixpanel <services/mixpanel>`::

	MIXPANEL_TOKEN = '0123456789abcdef0123456789abcdef'

* :doc:`Optimizely <services/optimizely>`::

	OPTIMIZELY_ACCOUNT_NUMBER = '1234567'


Configuring behavior
--------------------

By default, django-analytical will comment out the service
initialization code if the client IP address is detected as one from the
:data:`ANALYTICAL_INTERNAL_IPS` setting, which is set to
:data:`INTERNAL_IPS` by default.

Also, if the visitor is a logged in user and the user is accessible in
the template context, the username is passed to the analytics services
that support identifying users.  See :data:`ANALYTICAL_AUTO_IDENTIFY`.

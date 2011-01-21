Installation and global configuration
=====================================

Integration of your analytics service is very simple.  There are four
steps: installing the package, adding it to the list of installed Django
applications, adding the template tags to your base template, and adding
the identifiers for the services you use to the project settings.

#. `Installing the Python package`_
#. `Installing the Django application`_
#. `Adding the template tags to the base template`_
#. `Configuring global settings`_


Installing the Python package
-----------------------------

To install django-analytical the ``analytical`` package must be added to
the Python path.  You can install it directly from PyPI using
``easy_install``::

	$ easy_install django-analytical

You can also install directly from source. Download either the latest
stable version from PyPI_ or any release from GitHub_, or use Git to
get the development code::

	$ git clone https://github.com/jcassee/django-analytical.git

.. _PyPI: http://pypi.python.org/pypi/django-analytical/
.. _GitHub: http://github.com/jcassee/django-analytical

Then install by running the setup script::

	$ cd django-analytical
	$ python setup.py install


Installing the Django application
---------------------------------

After you install django-analytical, add the ``analytical`` Django
application to the list of installed applications in the ``settings.py``
file of your project::

	INSTALLED_APPS = [
		...
		'analytical',
		...
	]


Adding the template tags to the base template
---------------------------------------------

Because every analytics service has uses own specific Javascript code
that should be added to the top or bottom of either the head or body
of every HTML page, the django-analytical provides four general-purpose
tags that will render the code needed for the services you are using.
Your base template should look like this::

	{% load analytical %}
	<!DOCTYPE ... >
	<html>
		<head>
			{% analytical_head_top %}

			...

			{% analytical_head_bottom %}
		</head>
		<body>
			{% analytical_body_top %}

			...

			{% analytical_body_bottom %}
		</body>
	</html>


Configuring global settings
---------------------------

The next step is to :doc:`configure the services <services/index>`.

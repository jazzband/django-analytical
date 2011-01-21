Quick Start Guide
=================

If you do not need any advanced analytics tracking, installing
django-analytical is very simple.  To install django-analytical the
``analytical`` package must be added to the Python path.  You can
install it directly from PyPI using ``easy_install``::

	$ easy_install django-analytical

After you install django-analytical, add the ``analytical`` Django
application to the list of installed applications in the ``settings.py``
file of your project::

	INSTALLED_APPS = [
		...
		'analytical',
		...
	]

Now add the django-analytical template tags to your base template::

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

Finally, configure the analytics services you use in the project
``settings.py`` file.  This is a list of the settings required for the
different services::

	CLICKY_SITE_ID = 'xxxxxxxx'
	CRAZY_EGG_ACCOUNT_NUMBER = 'xxxxxxxx'
	GOOGLE_ANALYTICS_ACCOUNT_NUMBER = 'UA-xxxxxx-x'
	KISSINSIGHTS_ACCOUNT_NUMBER = 'xxxxx'
	KISSINSIGHTS_ACCOUNT_NUMBER = 'xxx'
	KISSINSIGHTS_ACCOUNT_NUMBER = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	MIXPANEL_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	OPTIMIZELY_ACCOUNT_NUMBER = 'xxxxxx'

Your analytics services are now installed.  Take a look at the rest of
the documentation for more information about further configuration and
customization of the various services.

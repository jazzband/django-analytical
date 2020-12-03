==============================
Installation and configuration
==============================

Integration of your analytics service is very simple.  There are four
steps: installing the package, adding it to the list of installed Django
applications, adding the template tags to your base template, and
configuring the services you use in the project settings.

#. `Installing the Python package`_
#. `Installing the Django application`_
#. `Adding the template tags to the base template`_
#. `Enabling the services`_


.. _installing-the-package:

Installing the Python package
=============================

To install django-analytical the ``analytical`` package must be added to
the Python path.  You can install it directly from PyPI using
``easy_install``:

.. code-block:: bash

    $ easy_install django-analytical

You can also install directly from source.  Download either the latest
stable version from PyPI_ or any release from GitHub_, or use Git to
get the development code:

.. code-block:: bash

    $ git clone https://github.com/jazzband/django-analytical.git

.. _PyPI: http://pypi.python.org/pypi/django-analytical/
.. _GitHub: http://github.com/jazzband/django-analytical

Then install the package by running the setup script:

.. code-block:: bash

    $ cd django-analytical
    $ python setup.py install


.. _installing-the-application:

Installing the Django application
=================================

After you installed django-analytical, add the ``analytical`` Django
application to the list of installed applications in the ``settings.py``
file of your project:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'analytical',
        ...
    ]


.. _adding-the-template-tags:

Adding the template tags to the base template
=============================================

Because every analytics service uses own specific Javascript code that
should be added to the top or bottom of either the head or body of the
HTML page, django-analytical provides four general-purpose template tags
that will render the code needed for the services you are using.  Your
base template should look like this:

.. code-block:: django

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

Instead of using the generic tags, you can also just use tags specific
for the analytics service(s) you are using.  See :ref:`services` for
documentation on using individual services.


.. _enabling-services:

Enabling the services
=====================

Without configuration, the template tags all render the empty string.
Services are configured in the project ``settings.py`` file.  The
settings required to enable each service are listed here:

* :doc:`Chartbeat <services/chartbeat>`::

    CHARTBEAT_USER_ID = '12345'

* :doc:`Clickmap <services/clickmap>`::

    CLICKMAP_TRACKER_CODE = '12345678....912'

* :doc:`Clicky <services/clicky>`::

    CLICKY_SITE_ID = '12345678'

* :doc:`Crazy Egg <services/crazy_egg>`::

    CRAZY_EGG_ACCOUNT_NUMBER = '12345678'

* :doc:`Facebook Pixel <services/facebook_pixel>`::

    FACEBOOK_PIXEL_ID = '1234567890'

* :doc:`Gaug.es <services/gauges>`::

    GAUGES_SITE_ID = '0123456789abcdef0123456789abcdef'

* :doc:`Google Analytics (legacy) <services/google_analytics>`::

    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-1234567-8'

* :doc:`Google Analytics (gtag.js) <services/google_analytics_gtag>`::

    GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = 'UA-1234567-8'

* :doc:`Google Analytics (analytics.js) <services/google_analytics_js>`::

    GOOGLE_ANALYTICS_JS_PROPERTY_ID = 'UA-12345678-9'

* :doc:`HubSpot <services/hubspot>`::

    HUBSPOT_PORTAL_ID = '1234'
    HUBSPOT_DOMAIN = 'somedomain.web101.hubspot.com'

* :doc:`Intercom <services/intercom>`::

    INTERCOM_APP_ID = '0123456789abcdef0123456789abcdef01234567'

* :doc:`KISSinsights <services/kiss_insights>`::

    KISS_INSIGHTS_ACCOUNT_NUMBER = '12345'
    KISS_INSIGHTS_SITE_CODE = 'abc'

* :doc:`KISSmetrics <services/kiss_metrics>`::

    KISS_METRICS_API_KEY = '0123456789abcdef0123456789abcdef01234567'

* :doc:`Lucky Orange <services/luckyorange>`::

    LUCKYORANGE_SITE_ID = '123456'

* :doc:`Matomo (formerly Piwik) <services/matomo>`::

    MATOMO_DOMAIN_PATH = 'your.matomo.server/optional/path'
    MATOMO_SITE_ID = '123'

* :doc:`Mixpanel <services/mixpanel>`::

    MIXPANEL_API_TOKEN = '0123456789abcdef0123456789abcdef'

* :doc:`Olark <services/olark>`::

    OLARK_SITE_ID = '1234-567-89-0123'

* :doc:`Optimizely <services/optimizely>`::

    OPTIMIZELY_ACCOUNT_NUMBER = '1234567'

* :doc:`Performable <services/performable>`::

    PERFORMABLE_API_KEY = '123abc'

* :doc:`Piwik (deprecated, see Matomo) <services/piwik>`::

    PIWIK_DOMAIN_PATH = 'your.piwik.server/optional/path'
    PIWIK_SITE_ID = '123'

* :doc:`Rating\@Mail.ru <services/rating_mailru>`::

    RATING_MAILRU_COUNTER_ID = '1234567'

* :doc:`SnapEngage <services/snapengage>`::

    SNAPENGAGE_WIDGET_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

* :doc:`Woopra <services/woopra>`::

    WOOPRA_DOMAIN = 'abcde.com'

* :doc:`Yandex.Metrica <services/yandex_metrica>`::

    YANDEX_METRICA_COUNTER_ID = '12345678'

----

The django-analytical application is now set-up to track visitors.  For
information about identifying users, further configuration and
customization, see :doc:`features`.

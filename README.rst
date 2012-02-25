django-analytical
=================

The django-analytical application integrates analytics services into a
Django_ project.

Using an analytics service with a Django project means adding Javascript
tracking code to the project templates.  Of course, every service has
its own specific installation instructions.  Furthermore, you need to
include your unique identifiers, which then end up in the templates.
Not very nice.

This application hides the details of the different analytics services
behind a generic interface, and keeps personal information and
configuration out of the templates.  Its goal is to make the basic
set-up very simple, while allowing advanced users to customize tracking.
Each service is set up as recommended by the services themselves, using
an asynchronous version of the Javascript code if possible.

Currently supported services:

* `Chartbeat`_ traffic analysis
* `Clicky`_ traffic analysis
* `Crazy Egg`_ visual click tracking
* `Gaug.es`_ realtime traffic tracking
* `Google Analytics`_ traffic analysis
* `GoSquared`_ traffic monitoring
* `HubSpot`_ inbound marketing
* `KISSinsights`_ feedback surveys
* `KISSmetrics`_ funnel analysis
* `Mixpanel`_ event tracking
* `Olark`_ visitor chat
* `Optimizely`_ A/B testing
* `Performable`_ web analytics and landing pages
* `Reinvigorate`_ visitor tracking
* `SnapEngage`_ live chat
* `Spring Metrics`_ conversion tracking
* `Woopra`_ web analytics

The documentation can be found in the ``docs`` directory or `read
online`_.  The source code and issue tracker are generously `hosted by
GitHub`_.

If you want to help out with the development of django-analytical, by
posting detailed bug reports, proposing new features or other analytics
services to support, or suggesting documentation improvements, use the
`issue tracker`_.  If you want to get your hands dirty, great!  Clone
the repository, make changes and send a pull request.  Please do create
an issue to discuss your plans.

.. _Django: http://www.djangoproject.com/
.. _Chartbeat: http://www.chartbeat.com/
.. _Clicky: http://getclicky.com/
.. _`Crazy Egg`: http://www.crazyegg.com/
.. _`Google Analytics`: http://www.google.com/analytics/
.. _`Gaug.es`: http://www.gaug.es/
.. _GoSquared: http://www.gosquared.com/
.. _HubSpot: http://www.hubspot.com/
.. _KISSinsights: http://www.kissinsights.com/
.. _KISSmetrics: http://www.kissmetrics.com/
.. _Mixpanel: http://www.mixpanel.com/
.. _Olark: http://www.olark.com/
.. _Optimizely: http://www.optimizely.com/
.. _Performable: http://www.performable.com/
.. _Reinvigorate: http://www.reinvigorate.com/
.. _SnapEngage: http://www.snapengage.com/
.. _`Spring Metrics`: http://www.springmetrics.com/
.. _Woopra: http://www.woopra.com/
.. _`read online`: http://packages.python.org/django-analytical/
.. _`hosted by GitHub`: http://github.com/jcassee/django-analytical
.. _`issue tracker`: http://github.com/jcassee/django-analytical/issues

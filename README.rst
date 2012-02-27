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
* `UserVoice`_ user feedback and helpdesk
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

.. _`Django`: http://www.djangoproject.com/
.. _`Chartbeat`: http://www.chartbeat.com/
.. _`Clicky`: http://getclicky.com/
.. _`Crazy Egg`: http://www.crazyegg.com/
.. _`Gaug.es`: http://gaug.es/
.. _`Google Analytics`: http://www.google.com/analytics/
.. _`GoSquared`: http://www.gosquared.com/
.. _`HubSpot`: http://www.hubspot.com/
.. _`KISSinsights`: http://www.kissinsights.com/
.. _`KISSmetrics`: http://www.kissmetrics.com/
.. _`Mixpanel`: http://www.mixpanel.com/
.. _`Olark`: http://www.olark.com/
.. _`Optimizely`: http://www.optimizely.com/
.. _`Performable`: http://www.performable.com/
.. _`Reinvigorate`: http://www.reinvigorate.com/
.. _`SnapEngage`: http://www.snapengage.com/
.. _`Spring Metrics`: http://www.springmetrics.com/
.. _`UserVoice`: http://www.uservoice.com/
.. _`Woopra`: http://www.woopra.com/

.. _`read online`: http://packages.python.org/django-analytical/
.. _`hosted by GitHub`: http://github.com/jcassee/django-analytical
.. _`issue tracker`: http://github.com/jcassee/django-analytical/issues

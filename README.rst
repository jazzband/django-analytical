django-analytical |latest-version|
==================================

|build-status| |coverage| |python-support| |license| |gitter| |jazzband|

The django-analytical application integrates analytics services into a
Django_ project.

.. start docs include

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

.. end docs include

.. |latest-version| image:: https://img.shields.io/pypi/v/django-analytical.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/django-analytical/
.. |build-status| image:: https://github.com/jazzband/django-analytical/workflows/Test/badge.svg
   :target: https://github.com/jazzband/django-analytical/actions
   :alt: GitHub Actions
.. |coverage| image:: https://codecov.io/gh/jazzband/django-analytical/branch/main/graph/badge.svg
   :alt: Test coverage
   :target: https://codecov.io/gh/jazzband/django-analytical
.. |python-support| image:: https://img.shields.io/pypi/pyversions/django-analytical.svg
   :target: https://pypi.org/project/django-analytical/
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/django-analytical.svg
   :alt: Software license
   :target: https://github.com/jazzband/django-analytical/blob/main/LICENSE.txt
.. |gitter| image:: https://img.shields.io/gitter/room/jazzband/django-analytical.svg
   :alt: Gitter chat room
   :target: https://gitter.im/jazzband/django-analytical
.. |jazzband| image:: https://jazzband.co/static/img/badge.svg
   :alt: Jazzband
   :target: https://jazzband.co/
.. _`Django`: http://www.djangoproject.com/

Currently Supported Services
----------------------------

* `Chartbeat`_ traffic analysis
* `Clickmap`_ visual click tracking
* `Clicky`_ traffic analysis
* `Crazy Egg`_ visual click tracking
* `Facebook Pixel`_ advertising analytics
* `Gaug.es`_ real time web analytics
* `Google Analytics`_ traffic analysis
* `GoSquared`_ traffic monitoring
* `Heap`_ analytics and events tracking
* `Hotjar`_ analytics and user feedback
* `HubSpot`_ inbound marketing
* `Intercom`_ live chat and support
* `KISSinsights`_ feedback surveys
* `KISSmetrics`_ funnel analysis
* `Lucky Orange`_ analytics and user feedback
* `Mixpanel`_ event tracking
* `Olark`_ visitor chat
* `Optimizely`_ A/B testing
* `Performable`_ web analytics and landing pages
* `Matomo (formerly Piwik)`_ open source web analytics
* `Rating\@Mail.ru`_ web analytics
* `SnapEngage`_ live chat
* `Spring Metrics`_ conversion tracking
* `UserVoice`_ user feedback and helpdesk
* `Woopra`_ web analytics
* `Yandex.Metrica`_ web analytics

.. _`Chartbeat`: http://www.chartbeat.com/
.. _`Clickmap`: http://clickmap.ch/
.. _`Clicky`: http://getclicky.com/
.. _`Crazy Egg`: http://www.crazyegg.com/
.. _`Facebook Pixel`: https://developers.facebook.com/docs/facebook-pixel/
.. _`Gaug.es`: http://get.gaug.es/
.. _`Google Analytics`: http://www.google.com/analytics/
.. _`GoSquared`: http://www.gosquared.com/
.. _`Heap`: https://heapanalytics.com/
.. _`Hotjar`: https://www.hotjar.com/
.. _`HubSpot`: http://www.hubspot.com/
.. _`Intercom`: http://www.intercom.io/
.. _`KISSinsights`: http://www.kissinsights.com/
.. _`KISSmetrics`: http://www.kissmetrics.com/
.. _`Lucky Orange`: http://www.luckyorange.com/
.. _`Mixpanel`: http://www.mixpanel.com/
.. _`Olark`: http://www.olark.com/
.. _`Optimizely`: http://www.optimizely.com/
.. _`Performable`: http://www.performable.com/
.. _`Matomo (formerly Piwik)`: https://matomo.org
.. _`Rating\@Mail.ru`: http://top.mail.ru/
.. _`SnapEngage`: http://www.snapengage.com/
.. _`Spring Metrics`: http://www.springmetrics.com/
.. _`UserVoice`: http://www.uservoice.com/
.. _`Woopra`: http://www.woopra.com/
.. _`Yandex.Metrica`: http://metrica.yandex.com

Documentation and Support
-------------------------

The documentation can be found in the ``docs`` directory or `read
online`_.  The source code and issue tracker are generously `hosted by
GitHub`_.  Bugs should be reported there, whereas for lengthy chats
and coding support when implementing new service integrations you're
welcome to use our `Gitter chat room`_.

.. _`read online`: https://django-analytical.readthedocs.io/
.. _`hosted by GitHub`: https://github.com/jazzband/django-analytical
.. _`Gitter chat room`: https://gitter.im/jazzband/django-analytical

How To Contribute
-----------------

.. start contribute include

If you want to help out with the development of django-analytical, by
posting detailed bug reports, proposing new features or other analytics
services to support, or suggesting documentation improvements, use the
`issue tracker`_.  If you want to get your hands dirty, great!  Clone
the repository, make changes and place a `pull request`_.  Creating an
issue to discuss your plans is useful.

This is a `Jazzband`_ project.  By contributing you agree to abide by the
`Contributor Code of Conduct`_ and follow the `guidelines`_.

.. _`issue tracker`: https://github.com/jazzband/django-analytical/issues
.. _`pull request`: https://github.com/jazzband/django-analytical/pulls
.. _`Jazzband`: https://jazzband.co
.. _`Contributor Code of Conduct`: https://jazzband.co/about/conduct
.. _`guidelines`: https://jazzband.co/about/guidelines

.. end contribute include

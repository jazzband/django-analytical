Version 3.0.0
-------------
* Add support for Lucky Orange (Peter Bittner)
* Add missing instructions in Installation chapter of the docs (Peter Bittner)
* Migrate test setup to Pytest (David Smith, Peter Bittner, Pi Delport)
* Support Django 3.1 and Python 3.9, drop Django 1.11 and Python 2.7/3.5 (David Smith)
* Migrate from Travis CI to GitHub Actions (Jannis Leidel)
* Update accepted patterns (regex) for Google Analytics GTag (Taha Rushain)
* Scope Piwik warning to use of Piwik (Hugo Barrera)
* Add ``user_id`` to Google Analytics GTag (Sean Wallace)

Version 2.6.0
-------------
* Support Django 3.0 and Python 3.8, drop Django 2.1
* Add support for Google Analytics Tag Manager (Marc Bourqui)
* Add Matomo, the renamed version of Piwik (Scott Karlin)
* Move Joost's project over to the Jazzband

Version 2.5.0
-------------
* Add support for Google analytics.js (Marc Bourqui)
* Add support for Intercom HMAC identity verification (Pi Delport)
* Add support for Hotjar (Pi Delport)
* Make sure _trackPageview happens before other settings in Google Analytics
  (Diederik van der Boor)

Version 2.4.0
-------------
* Support Django 2.0 (Matthäus G. Chajdas)

Version 2.3.0
-------------
* Add Facebook Pixel support (Pi Delport)
* Add Python 3.6 and Django 1.10 & 1.11 tests (Pi Delport)
* Drop Python 3.2 support

Version 2.2.2
-------------
* Allow port in Piwik domain path. (Alex Ramsay)

Version 2.2.1
-------------
* Fix a bug with the extra Google Analytics variables also pushing the `_gat.`
  flag onto the configuration array.

Version 2.2.0
-------------
* Update Woopra JavaScript snippet (Aleck Landgraf)

Version 2.1.0
-------------
* Support Rating\@mail.ru (Nikolay Korotkiy)
* Support Yandex.Metrica (Nikolay Korotkiy)
* Add support for extra Google Analytics variables (Steve Schwarz)
* Remove support for Reinvigorate (service shut down)

Version 2.0.0
-------------
* Support Django 1.9, drop support for Django < 1.7 (Hugo Osvaldo Barrera)
* Support custom user models with an alternative username field (Brad Pitcher)

Version 1.0.0
-------------
* Add Piwik user variables support (Alexandre Pocquet)

Version 0.22.0
--------------
* Mark package as Python 3 compatible (Martín Gaitán)
* Fix Clickmap tracker id regular expression
* Test with Django 1.8

Version 0.21.0
--------------
* Added compatibility with Python 3 (Eric Amador)

Version 0.20.0
--------------
* Support Django 1.7 (Craig Bruce)
* Update Mixpanel identity code (Martín Gaitán)
* Identify authenticated users in Uservoice (Martín Gaitán)
* Add full name and email to Olark (Scott Adams)

Version 0.19.0
--------------
* Add Piwik integration (Peter Bittner)

Version 0.18.0
--------------
* Update HubSpot code (Craig Bruce)

Version 0.17.1
--------------
* Fix typo in Intercom.io support (Steven Skoczen)

Version 0.17.0
--------------
* Update UserVoice support (Martín Gaitán)
* Add support for Intercom.io (Steven Skoczen)

Version 0.16.0
--------------
* Add support for GA Display Advertising features (Max Arnold)

Version 0.15.0
--------------
* Add IP anonymization setting to GA tracking pixel (Tinnet Coronam)
* Include Django 1.5 in tox.ini (Tinnet Coronam)
* Add Clickmap integration (Philippe O. Wagner)

Version 0.14.0
--------------
* Update mixpanel integration to latest code (Simon Ye)

Version 0.13.0
--------------
* Add support for the KISSmetrics alias feature (Sandra Mau)
* Update testing code for Django 1.4 (Pi Delport)

Version 0.12.0
--------------
* Add support for the UserVoice service.

Version 0.11.3
--------------
* Added support for Gaug.es (Steven Skoczen)

Version 0.11.2
--------------
* Fix Spring Metrics custom variables.
* Update Spring Metrics documentation.

Version 0.11.1
--------------
* Fix Woopra for anonymous users (Steven Skoczen).

Version 0.11.0
--------------
* Added support for the Spring Metrics service.
* Allow sending events and properties to KISSmetrics (Paul Oswald).
* Add support for the Site Speed report in Google Analytics (Uros
  Trebec).

Version 0.10.0
--------------
* Added multiple domains support for Google Analytics.
* Fixed bug in deleted settings testing code (Eric Davis).

Version 0.9.2
-------------
* Added support for the SnapEngage service.
* Updated Mixpanel code (Julien Grenier).

Version 0.9.1
-------------
* Fixed compatibility with Python 2.5 (Iván Raskovsky).

Version 0.9.0
-------------
* Updated Clicky tracking code to support multiple site ids.
* Fixed Chartbeat auto-domain bug when the Sites framework is not used
  (Eric Davis).
* Improved testing code (Eric Davis).

Version 0.8.1
-------------
* Fixed MANIFEST bug that caused GoSquared support to be missing from
  the source distribution.

Version 0.8.0
-------------
* Added support for the GoSquared service.
* Updated Clicky tracking code to use relative URLs.

Version 0.7.0
-------------
* Added support for the Woopra service.
* Added chat window text customization to Olark.
* Renamed ``MIXPANEL_TOKEN`` setting to ``MIXPANEL_API_TOKEN`` for
  compatibility with Wes Winham's mixpanel-celery_ package.
* Fixed the ``<script>`` tag for Crazy Egg.

.. _mixpanel-celery: https://github.com/winhamwr/mixpanel-celery

Version 0.6.0
-------------
* Added support for the Reinvigorate service.
* Added support for the Olark service.

Version 0.5.0
-------------
* Split off Geckoboard support into django-geckoboard_.

.. _django-geckoboard: http://pypi.python.org/pypi/django-geckoboard

Version 0.4.0
-------------
* Added support for the Geckoboard service.

Version 0.3.0
-------------
* Added support for the Performable service.

Version 0.2.0
-------------
* Added support for the HubSpot service.
* Added template tags for individual services.

Version 0.1.0
-------------
* First project release.

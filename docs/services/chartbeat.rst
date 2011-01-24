Chartbeat -- traffic analysis
=============================

Chartbeat_ provides real-time analytics to websites and blogs.  It shows
visitors, load times, and referring sites on a minute-by-minute basis.
The service also provides alerts the second your website crashes or
slows to a crawl.

.. _Chartbeat: http://www.chartbeat.com/

The Chartbeat service adds code both to the top of the head section and
the bottom of the body section.  If the project uses the sites
framework, the domain name of the current website will be passed to
Chartbeat.  Otherwise, Chartbeat will detect the domain name from the
URL.


Required settings
-----------------

.. data:: CHARTBEAT_USER_ID

  The User ID::

      CHARTBEAT_USER_ID = '12345'

  You can find the User ID by visiting the Chartbeat `Add New Site`_
  page.  The second code snippet contains a line that looks like this::

  	  var _sf_async_config={uid:XXXXX,domain:"YYYYYYYYYY"};

  Here, ``XXXXX`` is your User ID.

.. _`Add New Site`: http://chartbeat.com/code/

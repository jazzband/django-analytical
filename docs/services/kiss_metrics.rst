KISSmetrics -- funnel analysis
==============================

KISSmetrics_ is an easy to implement analytics solution that provides a
powerful visual representation of your customer lifecycle.  Discover how
many visitors go from your landing page to pricing to sign up, and how
many drop out at each stage.

.. _KISSmetrics: http://www.kissmetrics.com/

The code is added to the top of the HTML head.  By default, the
username of a logged-in user is passed to KISSmetrics.  See
:data:`ANALYTICAL_AUTO_IDENTIFY`.


Required settings
-----------------

.. data:: KISSMETRICS_API_KEY

  The website API key::

      KISSMETRICS_API_KEY = '1234567890abcdef1234567890abcdef12345678'

  You can find the website API key by visiting the website `Product
  center` on your KISSmetrics dashboard.

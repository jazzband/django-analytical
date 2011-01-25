Clicky -- traffic analysis
==========================

Clicky_ is an online web analytics tool.  It is similar to Google
Analytics in that it provides statistics on who is visiting your website
and what they are doing.  Clicky provides its data in real time and is
designed to be very easy to use.

.. _Clicky: http://getclicky.com/

The setup code is added to the bottom of the HTML body.  By default, the
username of a logged-in user is passed to Clicky.  See
:data:`ANALYTICAL_AUTO_IDENTIFY`.


Required settings
-----------------

.. data:: CLICKY_SITE_ID

  The Clicky site identifier, or Site ID::

      CLICKY_SITE_ID = '12345678'

  You can find the Site ID in the Info tab of the website Preferences
  page on your Clicky account.

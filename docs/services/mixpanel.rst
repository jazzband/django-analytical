Mixpanel -- event tracking
==========================

Mixpanel_ tracks events and actions to see what features users are using
the most and how they are trending.  You could use it for real-time
analysis of visitor retention or funnels.

.. _Mixpanel: http://www.mixpanel.com/

The code is added to the bottom of the HTML head.  By default, the
username of a logged-in user is passed to Mixpanel.  See
:data:`ANALYTICAL_AUTO_IDENTIFY`.


Required settings
-----------------

.. data:: MIXPANEL_TOKEN

  The website project token ::

      MIXPANEL_TOKEN = '1234567890abcdef1234567890abcdef'

  You can find the project token on the Mixpanel `projects` page.

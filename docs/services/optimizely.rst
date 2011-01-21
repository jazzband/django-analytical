Optimizely -- A/B testing
=========================

Optimizely_ is an easy way to implement A/B testing.  Try different
decisions, images, layouts, and copy without touching your website code
and see exactly how your experiments are affecting pagevieuws,
retention and sales.

.. _Optimizely: http://www.optimizely.com/


Required settings
-----------------

.. data:: OPTIMIZELY_ACCOUNT_NUMBER

  The website project token ::

      OPTIMIZELY_ACCOUNT_NUMBER = '1234567'

  You can find your account number by clicking the `Implementation` link
  in the top right-hand corner of the Optimizely website.  A pop-up
  window will appear containing HTML code looking like this:
  ``<script src="//cdn.optimizely.com/js/XXXXXXX.js"></script>``.
  The number ``XXXXXXX`` is your account number.

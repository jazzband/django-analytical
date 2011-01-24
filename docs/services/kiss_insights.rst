KISSinsights -- feedback surveys
================================

KISSinsights_ provides unobtrusive surveys that pop up from the bottom
right-hand corner of your website.  Asking specific questions gets you
the targeted, actionable feedback you need to make your site better.

.. _KISSinsights: http://www.kissinsights.com/


Required settings
-----------------

.. data:: KISSINSIGHTS_ACCOUNT_NUMBER

  The KISSinsights account number::

      KISSINSIGHTS_ACCOUNT_NUMBER = '12345'

.. data:: KISSINSIGHTS_SITE_CODE

  The KISSinsights website code::

      KISSINSIGHTS_SITE_CODE = 'abc'

You can find the account number and website code by visiting the code
installation page of the website you want to place the surveys on.  You
will see some HTML code with a Javascript tag with a ``src`` attribute
containing ``//s3.amazonaws.com/ki.js/XXXXX/YYY.js``.  Here ``XXXXX`` is
the account number and ``YYY`` the website code.

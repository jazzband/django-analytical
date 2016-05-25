===================================
Rating\@Mail.ru -- traffic analysis
===================================

`Rating\@Mail.ru`_ is an analytics tool like as google analytics.

.. _`Rating\@Mail.ru`: http://top.mail.ru/


.. rating-mailru-installation:

Installation
============

To start using the Rating\@Mail.ru integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Rating\@Mail.ru template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`rating-mailru-configuration`.

The Rating\@Mail.ru counter code is inserted into templates using a template
tag.  Load the :mod:`rating_mailru` template tag library and insert the
:ttag:`rating_mailru` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML head::

    {% load rating_mailru %}
    <html>
    <head>
    ...
    {% rating_mailru %}
    </head>
    ...


.. _rating-mailru-configuration:

Configuration
=============

Before you can use the Rating\@Mail.ru integration, you must first set
your website counter ID.


.. _rating-mailru-counter-id:

Setting the counter ID
----------------------

Every website you track with Rating\@Mail.ru gets its own counter ID,
and the :ttag:`rating_mailru` tag will include it in the rendered
Javascript code.  You can find the web counter ID on the overview page
of your account.  Set :const:`RATING_MAILRU_COUNTER_ID` in the
project :file:`settings.py` file::

    RATING_MAILRU_COUNTER_ID = '1234567'

If you do not set a counter ID, the counter code will not be rendered.

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`RATING_MAILRU_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

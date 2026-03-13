==================================
Liveinternet -- traffic analysis
==================================


`Liveinternet`_ is an analytics tool like as google analytics.

.. _`Liveinternet`: https://www.liveinternet.ru/code/


.. yandex-metrica-installation:

Installation
============

To start using the Liveinternet integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Liveinternet template tag to your templates.

The Liveinternet counter code is inserted into templates using a template
tag.  Load the :mod:`liveinternet` template tag library and insert the
:ttag:`liveinternet` tag.  To display as a single image combining a counter
and the LiveInternet logo::

    {% load liveinternet %}
    <html>
    <head>
    ...
    {% liveinternet %}
    </head>
    ...

In the form of two images, one of which is a counter (transparent GIF size 1x1),
and the other is the LiveInternet logo. This placement method will allow you to
insert the code of the invisible counter at the beginning of the page, and the
logo - where the design and content of the page allows. ::

    {% load liveinternet %}
    <html>
    <head>
    ...
    {% liveinternet_code %}
    </head>
    <body>
    ...
        {% liveinternet_img %}
    ...
    </body>


Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.
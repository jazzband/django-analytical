=====================================
Heap -- analytics and events tracking
=====================================

`Heap`_ automatically captures all user interactions on your site, from the moment of installation forward. 

.. _`Heap`: https://heap.io/


.. heap-installation:

Installation
============

To start using the Heap integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

.. _heap-configuration:

Configuration
=============

Before you can use the Heap integration, you must first get your
Heap Tracker ID. If you don't have a Heap account yet,
`sign up`_ to get your Tracker ID.

.. _`sign up`: https://heap.io/


.. _heap-tracker-id:

Setting the Tracker ID
----------------------

Heap gives you a unique ID. You can find this ID on the Projects page
of your Heap account. Set :const:`HEAP_TRACKER_ID` in the project
:file:`settings.py` file::

    HEAP_TRACKER_ID = 'XXXXXXXX'

If you do not set an Tracker ID, the tracking code will not be
rendered.

The tracking code will be added just before the closing head tag.


.. _heap-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`ANALYTICAL_INTERNAL_IPS` setting
(which is :const:`INTERNAL_IPS` by default,) the tracking code is 
commented out. See :ref:`identifying-visitors` for important information
about detecting the visitor IP address.

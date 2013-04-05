==================================
Clickmap -- visual click tracking
==================================

`Clickmap`_ is a real-time heatmap tool to track mouse clicks and scroll paths of your website visitors. Gain intelligence about what's hot and what's not, and optimize your conversion with Clickmap.

.. _`Clickmap`: http://www.getclickmap.com/


.. clickmap-installation:

Installation
============

To start using the Clickmap integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Clickmap template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`clickmap-configuration`.

The Clickmap Javascript code is inserted into templates using a template
tag. Load the :mod:`clickmap` template tag library and insert the
:ttag:`clickmap` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template. Insert
the tag at the bottom of the HTML body::

    {% load clickmap %}
    ...
    {% clickmap %}
    </body>
    </html>


.. _clickmap-configuration:

Configuration
=============

Before you can use the Clickmap integration, you must first set your
Clickmap Tracker ID. If you don't have a Clickmap account yet,
`sign up`_ to get your Tracker ID.

.. _`sign up`: http://www.getclickmap.com/


.. _clickmap-tracker-id:

Setting the Tracker ID
----------------------

Clickmap gives you a unique Tracker ID, and the :ttag:`clickmap`
tag will include it in the rendered Javascript code. You can find your
Tracker ID clicking the link named "Tracker" in the dashboard
of your Clickmap account. Set :const:`CLICKMAP_TRACKER_ID` in the project
:file:`settings.py` file::

    CLICKMAP_TRACKER_ID = 'XXXXXXXX'

If you do not set an Tracker ID, the tracking code will not be
rendered.


.. _clickmap-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`ANALYTICAL_INTERNAL_IPS` setting
(which is :const:`INTERNAL_IPS` by default,) the tracking code is 
commented out. See :ref:`identifying-visitors` for important information
about detecting the visitor IP address.

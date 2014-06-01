============================
HubSpot -- inbound marketing
============================

HubSpot_ helps you get found by customers.  It provides tools for
content creation, conversion and marketing analysis.  HubSpot uses
tracking on your website to measure effect of your marketing efforts.

.. _HubSpot: http://www.hubspot.com/


.. hubspot-installation:

Installation
============

To start using the HubSpot integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the HubSpot template tag to your templates. This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`hubspot-configuration`.

The HubSpot tracking code is inserted into templates using a template
tag.  Load the :mod:`hubspot` template tag library and insert the
:ttag:`hubspot` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body::

    {% load hubspot %}
    ...
    {% hubspot %}
    </body>
    </html>


.. _hubspot-configuration:

Configuration
=============

Before you can use the HubSpot integration, you must first set your
portal ID, also known as your Hub ID.


.. _hubspot-portal-id:

Setting the portal ID
---------------------

Your HubSpot account has its own portal ID, the :ttag:`hubspot` tag
will include them in the rendered JavaScript code. You can find the
portal ID by accessing your dashboard. Alternatively, read this
`Quick Answer page <http://help.hubspot.com/articles/KCS_Article/Where-can-I-find-my-HUB-ID>`_.
Set :const:`HUBSPOT_PORTAL_ID` in the project :file:`settings.py` file::

    HUBSPOT_PORTAL_ID = 'XXXX'

If you do not set the portal ID, the tracking code will not be rendered.


.. deprecated:: 0.18.0
    `HUBSPOT_DOMAIN` is no longer required.

.. _hubspot-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`HUBSPOT_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

============================
HubSpot -- inbound marketing
============================

HubSpot_ helps you get found by customers.  It provides tools for
content creation, convertion and marketing analysis.  HubSpot uses
tracking on your website to measure effect of your marketing efforts.

.. _HubSpot: http://www.hubspot.com/


.. hubspot-installation:

Installation
============

You only need to do perform these steps if you are not using the
generic :ttag:`analytical.*` tags.  If you are, skip to
:ref:`hubspot-configuration`.

In order to use the template tag, you need to add :mod:`analytical` to
the installed applications list in the project :file:`settings.py`
file::

    INSTALLED_APPS = [
        ...
        'analytical',
        ...
    ]

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
portal ID and domain.


.. _hubspot-portal-id:

Setting the portal ID and domain
--------------------------------

Your HubSpot account has its own portal ID and primary websit, and the
:ttag:`hubspot` tag will include them in the rendered Javascript code.
You can find the portal ID and domain by going to the *Domains* tab in
your HubSpot account.  The domain you need to use is listed as *Primary
Domain* on that page, and the portal ID can be found in the footer.  Set
:const:`HUBSPOT_PORTAL_ID` and :const:`HUBSPOT_DOMAIN` in the
project :file:`settings.py` file::

    HUBSPOT_PORTAL_ID = 'XXXX'
    HUBSPOT_DOMAIN = 'XXXXXXXX.web101.hubspot.com'

If you do not set the portal ID and domain, the tracking code will not
be rendered.


.. _hubspot-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`INTERNAL_IPS` setting, the
tracking code is commented out.  See :const:`ANALYTICAL_INTERNAL_IPS`
for important information about detecting the visitor IP address.

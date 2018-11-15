=====================================
Hotjar -- analytics and user feedback
=====================================

`Hotjar`_ is a website analytics and user feedback tool.

.. _`Hotjar`: https://www.hotjar.com/


.. hotjar-installation:

Installation
============

To start using the Hotjar integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Hotjar template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`hotjar-configuration`.

The Hotjar code is inserted into templates using template tags.
Because every page that you want to track must have the tag,
it is useful to add it to your base template.
At the top of the template, load the :mod:`hotjar` template tag library.
Then insert the :ttag:`hotjar` tag at the bottom of the head section::

    {% load hotjar %}
    <html>
    <head>
    ...
    {% hotjar %}
    </head>
    ...
    </html>


.. _hotjar-configuration:

Configuration
=============

Before you can use the Hotjar integration, you must first set your Site ID.


.. _hotjar-id:

Setting the Hotjar Site ID
--------------------------

You can find the Hotjar Site ID in the "Sites & Organizations" section of your Hotjar account.
Set :const:`HOTJAR_SITE_ID` in the project :file:`settings.py` file::

    HOTJAR_SITE_ID = 'XXXXXXXXX'

If you do not set a Hotjar Site ID, the code will not be rendered.


.. _hotjar-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`HOTJAR_INTERNAL_IPS`
setting, the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.

=============================
Gaug.es -- Real-time tracking
=============================

Gaug.es_ is an easy way to implement real-time tracking for multiple
websites.

.. _Gaug.es: http://www.gaug.es/


.. gauges-installation:

Installation
============

To start using the Gaug.es integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Gaug.es template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`gauges-configuration`.

The Gaug.es Javascript code is inserted into templates using a
template tag.  Load the :mod:`gauges` template tag library and
insert the :ttag:`gauges` tag.  Because every page that you want to
track must have the tag, it is useful to add it to your base template.
Insert the tag at the top of the HTML head::

    {% load gauges %}
    <html>
    <head>
    {% gauges %}
    ...


.. _gauges-configuration:

Configuration
=============

Before you can use the Gaug.es integration, you must first set your
site id.


.. _gauges-site-id:

Setting the site id
--------------------------

Gaug.es gives you a unique site id, and the :ttag:`gauges`
tag will include it in the rendered Javascript code.  You can find your
site id by clicking the *Tracking Code* link when logged into
the on the gaug.es website.  A page will display containing
HTML code looking like this::

    <script type="text/javascript">
      var _gauges = _gauges || [];
      (function() {
        var t   = document.createElement('script');
        t.type  = 'text/javascript';
        t.async = true;
        t.id    = 'gauges-tracker';
        t.setAttribute('data-site-id', 'XXXXXXXXXXXXXXXXXXXXXXX');
        t.src = '//secure.gaug.es/track.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(t, s);
      })();
    </script>

The code ``XXXXXXXXXXXXXXXXXXXXXXX`` is your site id.  Set
:const:`GAUGES_SITE_ID` in the project :file:`settings.py`
file::

    GAUGES_SITE_ID = 'XXXXXXXXXXXXXXXXXXXXXXX'

If you do not set an site id, the Javascript code will not be
rendered.


.. _gauges-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`ANALYTICAL_INTERNAL_IPS` setting
(which is :const:`INTERNAL_IPS` by default,) the tracking code is 
commented out. See :ref:`identifying-visitors` for important information
about detecting the visitor IP address.

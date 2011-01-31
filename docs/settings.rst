========
Settings
========

Here's a full list of all available settings, in alphabetical order, and
their default values.



.. data:: ANALYTICAL_AUTO_IDENTIFY

    Default: ``True``

    Automatically identify logged in users by their username.  See
    :ref:`identifying-visitors`.


.. data:: ANALYTICAL_INTERNAL_IPS

    Default: :data:`INTERNAL_IPS`

    A list or tuple of internal IP addresses.  	Tracking code will be
    commented out for visitors from any of these addresses.  You can
    configure this setting for each service individually by substituting
    ``ANALYTICAL`` for the upper-case service name.  For example, set
    ``GOOGLE_ANALYTICS_INTERNAL_IPS`` to configure for Google Analytics.

    See :ref:`internal-ips`.

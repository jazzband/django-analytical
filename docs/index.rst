========================================
Analytics service integration for Django
========================================

The django-analytical application integrates various analytics services
into a Django_ project.

.. _Django: http://www.djangoproject.com/

:Download: http://pypi.python.org/pypi/django-analytical/
:Source:   http://github.com/jcassee/django-analytical

Overview
========

If your want to integrating an analytics service into a Django project,
you need to add Javascript tracking code to the project templates.
Unfortunately, every services has its own specific installation
instructions.  Furthermore, you need to specify your unique identifiers
which would end up in templates.  This application hides the details of
the different analytics services behind a generic interface.  It is
designed to make the common case easy while allowing advanced users to
customize tracking.


Features
--------

* Easy installation.  See the :doc:`quick`.
* Supports many services.  See :doc:`services/index`.
* Automatically identifies logged-in users (not implemented yet)
* Disables tracking on internal IP addresses (not implemented yet)


Contents
========

.. toctree::
    :maxdepth: 2

    quick
    install
    services/index
    history

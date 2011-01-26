========================================
Analytics service integration for Django
========================================

The django-analytical application integrates various analytics services
into a Django_ project.

.. _Django: http://www.djangoproject.com/

:Package: http://pypi.python.org/pypi/django-analytical/
:Source:  http://github.com/jcassee/django-analytical


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

The application provides four generic template tags that are added to
the top and bottom of the head and body section of the base template.
Configured services will be enabled automatically by adding Javascript
code at these locations.  The installation will follow the
recommendations from the analytics services, using an asynchronous
version of the code if possible.  See :doc:`services/index` for detailed
information about each individual analytics service.


Contents
========

.. toctree::
    :maxdepth: 2

    install
    services/index
    settings
    history

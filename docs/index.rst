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
Of course, every service has its own specific installation instructions.
Furthermore, you need to include your unique identifiers, which then end
up in the templates.  This application hides the details of the
different analytics services behind a generic interface, and keeps
personal information and configuration out of the templates.  Its goal
is to make basic usage set-up very simple, while allowing advanced users
to customize tracking.  Each service is set up as recommended by the
services themselves, using an asynchronous version of the Javascript
code if possible.

To get a feel of how django-analytics works, check out the
:doc:`tutorial`.


Contents
========

.. toctree::
    :maxdepth: 2

    tutorial
    install
    features
    services
    settings
    history
    license

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
to customize tracking.  Each service is set-up as recommended by the
services themselves, using an asynchronous version of the Javascript
code if possible.

To get a feel of how django-analytics works, first check out the
:doc:`tutorial`.


Contents
========

.. toctree::
    :maxdepth: 2

    tutorial
    install
    services
    settings
    history


Helping out
===========

If you want to help out with development of django-analytical, by
posting detailed bug reports, suggesting new features or other analytics
services to support, or doing some development work yourself, please use
the `GitHub project page`_:

* Use the `issue tracker`_ to discuss bugs and features.
* If you want to do the work yourself, great! Clone the repository, make
  changes and send a pull request.  Please create a new issue first so
  that we can discuss it, and keep people from stepping on each others
  toes.
* Of course, you can always send ideas and patches to joost@cassee.net.

.. _`GitHub project page`: http://github.com/jcassee/django-analytical
.. _`issue tracker`: http://github.com/jcassee/django-analytical/issues

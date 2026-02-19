===================
History and credits
===================

Changelog
=========

The project follows the `Semantic Versioning`_ specification for its
version numbers.  Patch-level increments indicate bug fixes, minor
version increments indicate new functionality and major version
increments indicate backwards incompatible changes.

Version 1.0.0 is the last to support Django < 1.7.  Users of older Django
versions should stick to 1.0.0, and are encouraged to upgrade their setups.
Starting with 2.0.0, dropping support for obsolete Django versions is not
considered to be a backward-incompatible change.

.. _`Semantic Versioning`: http://semver.org/

.. include:: ../CHANGELOG.rst


Credits
=======

The django-analytical package was originally written by `Joost Cassee`_
and is now maintained by `Peter Bittner`_ and the `Jazzband community`_.
All known contributors are listed as ``authors`` in the `project metadata`_.

Included JavaScript code snippets for integration of the analytics services
were written by the respective service providers.

The application was inspired by and uses ideas from Analytical_, Joshua
Krall's all-purpose analytics front-end for Rails.

.. _`Joost Cassee`: https://github.com/jcassee
.. _`Peter Bittner`: https://github.com/bittner
.. _`Jazzband community`: https://jazzband.co/
.. _`project metadata`: https://github.com/jazzband/django-analytical/blob/main/pyproject.toml#L15-L60
.. _`Analytical`: https://github.com/jkrall/analytical

.. _helping-out:

Helping out
===========

.. include:: ../README.rst
    :start-after: .. start contribute include
    :end-before: .. end contribute include


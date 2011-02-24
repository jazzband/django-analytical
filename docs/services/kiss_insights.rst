================================
KISSinsights -- feedback surveys
================================

KISSinsights_ provides unobtrusive surveys that pop up from the bottom
right-hand corner of your website.  Asking specific questions gets you
the targeted, actionable feedback you need to make your site better.

.. _KISSinsights: http://www.kissinsights.com/


.. kiss-insights-installation:

Installation
============

To start using the KISSinsights integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the KISSinsights template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`kiss-insights-configuration`.

The KISSinsights survey code is inserted into templates using a template
tag.  Load the :mod:`kiss_insights` template tag library and insert the
:ttag:`kiss_insights` tag.  Because every page that you want to track
must have the tag, it is useful to add it to your base template.  Insert
the tag at the top of the HTML body::

    {% load kiss_insights %}
    ...
    </head>
    <body>
    {% kiss_insights %}
    ...


.. _kiss-insights-configuration:

Configuration
=============

Before you can use the KISSinsights integration, you must first set your
account number and site code.


.. _kiss-insights-account-number:

Setting the account number and site code
----------------------------------------

In order to install the survey code, you need to set your KISSinsights
account number and website code.  The :ttag:`kiss_insights` tag will
include it in the rendered Javascript code.  You can find the account
number and website code by visiting the code installation page of the
website you want to place the surveys on.  You will see some HTML code
with a Javascript tag with a ``src`` attribute containing
``//s3.amazonaws.com/ki.js/XXXXX/YYY.js``.  Here ``XXXXX`` is the
account number and ``YYY`` the website code.  Set
:const:`KISS_INSIGHTS_ACCOUNT_NUMBER` and
:const:`KISS_INSIGHTS_WEBSITE_CODE` in the project :file:`settings.py`
file::

    KISSINSIGHTS_ACCOUNT_NUMBER = 'XXXXX'
    KISSINSIGHTS_SITE_CODE = 'XXX'

If you do not set the account number and website code, the survey code
will not be rendered.


.. _kiss-insights-identity-user:

Identifying authenticated users
-------------------------------

If your websites identifies visitors, you can pass this information on
to KISSinsights so that you can tie survey submissions to customers.
By default, the username of an authenticated user is passed to
KISSinsights automatically.  See :ref:`identifying-visitors`.

You can also send the visitor identity yourself by adding either the
``kiss_insights_identity`` or the ``analytical_identity`` variable to
the template context.  If both variables are set, the former takes
precedence. For example::

    context = RequestContext({'kiss_insights_identity': identity})
    return some_template.render(context)

If you can derive the identity from the HTTP request, you can also use
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def identify(request):
        try:
            return {'kiss_insights_identity': request.user.email}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.


.. _kiss-insights-show-survey:

Showing a specific survey
-------------------------

KISSinsights can also be told to show a specific survey.  You can let
the :ttag:`kiss_insights` tag include the code to select a survey by
passing the survey ID to the template in the
``kiss_insights_show_survey`` context variable::

    context = RequestContext({'kiss_insights_show_survey': 1234})
    return some_template.render(context)

For information about how to find the survey ID, see the explanation
on `"How can I show a survey after a custom trigger condition?"`_ on the
KISSinsights help page.

.. _`"How can I show a survey after a custom trigger condition?"`: http://www.kissinsights.com/help#customer-trigger

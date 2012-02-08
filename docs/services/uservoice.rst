=======================================
UserVoice -- user feedback and helpdesk
=======================================

UserVoice_ makes it simple for your customers to give, discuss, and vote
for feedback.  An unobtrusive feedback button allows visitors to easily
submit and discuss ideas without  having to sign up for a new account.
The best ideas are delivered to you based on customer votes.

.. _UserVoice: http://www.uservoice.com/


Installation
============

To start using the UserVoice integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the UserVoice template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`uservoice-configuration`.

The UserVoice Javascript code is inserted into templates using a
template tag.  Load the :mod:`uservoice` template tag library and insert
the :ttag:`uservoice` tag.  Because every page that you want to have
the feedback button to appear on must have the tag, it is useful to add
it to your base template.  Insert the tag at the bottom of the HTML
body::

    {% load uservoice %}
    ...
    {% uservoice %}
    </body>
    </html>


.. _uservoice-configuration:

Configuration
=============

Before you can use the UserVoice integration, you must first set your
account name.


Setting the account name
------------------------

In order to load the Javascript code, you need to set your UserVoice
account name.  The account name is the username you use to log into
UserVoice with.  Set :const:`USERVOICE_ACCOUNT_NAME` in the project
:file:`settings.py` file::

    USERVOICE_ACCOUNT_NAME = 'XXXXX'

If you do not set the account name, the feedback button will not be
rendered.


.. _uservoice-hide:

Hiding the feedback button
--------------------------

The feedback button is shown on every page that has the template tag.
You can hide the button by default by setting :const:`USERVOICE_SHOW`
in the project :file:`settings.py` file::

    USERVOICE_SHOW = False

The feedback button is also automatically hidden if you add a custom
link to launch the widget by using the :ttag:`uservoice_link` template
tag.  (See :ref:`uservoice-link`.)  The :ttag:`uservoice` tag must
appear below it in the template, but its preferredlocation is the bottom
of the body HTML anyway.

You can hide the feedback button for a specific view you can do so by
passing the ``uservoice_show`` context variable::

    context = RequestContext({'uservoice_show': False})
    return some_template.render(context)

If you show or hide the feedback button based on some computable
condition, you may want to set variables in a context processor that you
add to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list in
:file:`settings.py`::

    def uservoice_show_to_staff(request):
        try:
            return {'uservoice_show': request.user.is_staff()}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.


.. _uservoice-link:

Using a custom link
-------------------

Instead of showing the default button, you can make the UserVoice widget
launch when a visitor clicks a link or on some other event occurs.  Use
the :ttag:`uservoice_link` in your template to render the Javascript
code to launch the widget::

    <a href="{% uservoice_link %}" title="Open feedback & support dialog (powered by UserVoice)">feedback & support</a>

If you use this tag and the :ttag:`uservoice` tag appears below it in
the HTML, the default button is automatically hidden.  See
:ref:`uservoice-link`.


Passing custom data into the helpdesk
-------------------------------------

You can pass custom data through your widget and into the ticketing
system.  First create custom fields in your `Ticket settings`_ page.
Deselect *Display on contact form* in the edit dialog for those fields
you intend to use from Django.  You can now pass values for this field
by passing the :data:`uservoice_fields` context variables to the
template::

    uservoice_fields = {
        'Type': 'Support Request',
        'Priority': 'High',
    }
    context = RequestContext({'uservoice_fields': uservoice_fields})
    return some_template.render(context)

You can instead use a context processor, but because of the way context
variables work in Django, you cannot use both.  The fields set in the
context processor will clobber all fields set in the
:class:`~django.template.context.RequestContext` constructor.


.. _`Ticket settings`: https://cassee.uservoice.com/admin/settings#/tickets



Using Single Sign-On
--------------------

If your websites authenticates users, you can allow them to use
UserVoice without having to create an account.

See also :ref:`identifying-visitors`.


----

Thanks go to UserVoice for their support with the development of this
application.

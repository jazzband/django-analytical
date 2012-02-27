=======================================
UserVoice -- user feedback and helpdesk
=======================================

UserVoice_ makes it simple for your customers to give, discuss, and vote
for feedback.  An unobtrusive feedback tab allows visitors to easily
submit and discuss ideas without  having to sign up for a new account.
The best ideas are delivered to you based on customer votes.

.. _UserVoice: http://www.uservoice.com/


.. _uservoice-installation:

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
the feedback tab to appear on must have the tag, it is useful to add
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

Before you can use the UserVoice integration, you must first set the
widget key.


Setting the widget key
----------------------

In order to use the feedback widget, you need to configure which widget
you want to show.  You can find the widget keys in the *Channels* tab on
your UserVoice *Settings* page.  Under the *Javascript Widget* heading,
find the Javascript embed code of the widget.  The widget key is the
alphanumerical string contained in the URL of the script imported by the
embed code::

    <script type="text/javascript">
      var uvOptions = {};
      (function() {
        var uv = document.createElement('script'); uv.type = 'text/javascript'; uv.async = true;
        uv.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'widget.uservoice.com/XXXXXXXXXXXXXXXXXXXX.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(uv, s);
      })();
    </script>

(The widget key is shown as ``XXXXXXXXXXXXXXXXXXXX``.)

The default widget
..................

Often you will use the same widget throughout your website.  The default
widget key is configured by setting :const:`USERVOICE_WIDGET_KEY` in
the project :file:`settings.py` file::

    USERVOICE_WIDGET_KEY = 'XXXXXXXXXXXXXXXXXXXX'

If the setting is present but empty, no widget is shown by default. This
is useful if you want to set a widget using a template context variable,
as the setting must be present for the generic :ttag:`analytical.*` tags
to work.

Per-view widget
...............

The widget key can by set in a view using the ``uservoice_widget_key``
template context variable::

    context = RequestContext({'uservoice_widget_key': 'XXXXXXXXXXXXXXXXXXXX'})
    return some_template.render(context)

The widget key passed in the context variable overrides the default
widget key.

Setting the widget key in a context processor
.............................................

You can also set the widget keys in a context processor that you add to
the :data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`.
For example, to show a specific widget to logged in users::

    def uservoice_widget_key(request):
        try:
            if request.user.is_authenticated():
                return {'uservoice_widget_key': 'XXXXXXXXXXXXXXXXXXXX'}
        except AttributeError:
            pass
        return {}

The widget key passed in the context variable overrides both the default
and the per-view widget key.


.. _uservoice-link:

Using a custom link
-------------------

Instead of showing the default feedback tab, you can make the UserVoice
widget launch when a visitor clicks a link or when some other event
occurs.  Use the :ttag:`uservoice_popup` tag in your template to render
the Javascript code to launch the widget::

    <a href="#" onclick="{% uservoice_popup %}; return false;">Feedback</a>

If you use this tag and the :ttag:`uservoice` tag appears below it in
the HTML, the default tab is automatically hidden.  (The preferred
location of the :ttag:`uservoice` is the bottom of the body HTML, so
this usually works automatically.)

You can explicitly hide the feedback tab by setting the
``uservoice_show_tab`` context variable to :const:`False`::

    context = RequestContext({'uservoice_show_tab': False})
    return some_template.render(context)

However, instead consider only setting the widget key in the views you
do want to show the widget on.


Showing a second widget
.......................

Use the :ttag:`uservoice_popup` tag with a widget_key to display a
different widget that the one configured in the
:const:`USERVOICE_WIDGET_KEY` setting or the ``uservoice_widget_key``
template context variable::

    <a href="#" onclick="{% uservoice_popup 'XXXXXXXXXXXXXXXXXXXX' %}; return false;">Helpdesk</a>

In this case, the default widget tab is not hidden.


Passing custom data into the helpdesk
-------------------------------------

You can pass custom data through your widget and into the ticketing
system.  First create custom fields in your *Tickets* settings page.
Deselect *Display on contact form* in the edit dialog for those fields
you intend to use from Django.  You can set values for this field by
passing the :data:`uservoice_fields` context variables to the
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


Using Single Sign-On
--------------------

If your websites authenticates users, you will be able to let them give
feedback without having to create a UserVoice account.

*This feature is in development*

See also :ref:`identifying-visitors`.


----

Thanks go to UserVoice for their support with the development of this
application.

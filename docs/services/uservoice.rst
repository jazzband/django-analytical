..
    After updating this file, remember to upload to the UserVoice
    knowledge base.

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

      UserVoice=window.UserVoice||[];(function(){
            var uv=document.createElement('script');uv.type='text/javascript';
            uv.async=true;uv.src='//widget.uservoice.com/XXXXXXXXXXXXXXXXXXXX.js';
            var s=document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(uv,s)})();
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

Widget options
..............

You can set :const:`USERVOICE_WIDGET_OPTIONS` to customize your widget
with UserVoice's options.

.. tip::

    See the `JS SDK Overview <https://developer.uservoice.com/docs/widgets/overview/>`_ and the `reference <https://developer.uservoice.com/docs/widgets/options/>`_ for the details of available options.

For example, to override the default position of the widget, you could define:

.. code-block:: python

    USERVOICE_WIDGET_OPTIONS = (('addTrigger',
                                 {"trigger_position": "bottom-left",
                                  "mode": "contact"}),)



Per-view widget
...............

The widget key can be set in a view using the ``uservoice_widget_key`` and
``uservoice_widget_options`` template context variables::

    context = RequestContext({'uservoice_widget_key': 'XXXXXXXXXXXXXXXXXXXX'})
    return some_template.render(context)

These variable passed in the context overrides the default
widget configuration.

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


In this case, the default widget tab is not hidden.



----

Thanks go to UserVoice for their support with the development of this
application.

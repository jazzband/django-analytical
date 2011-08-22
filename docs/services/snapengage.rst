=======================
SnapEngage -- live chat
=======================

SnapEngage_ is a live chat widget for your site which integrates with your
existing chat client.  It integrates with many online applications and even
allows you to make a remote screenshot of the webpage.  SnapEngage can be
customized to fit your website look and feel, offers reports and statistics and
is available in many languages.

.. _SnapEngage: http://www.snapengage.com/


Installation
============

To start using the SnapEngage integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the SnapEngage template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`snapengage-configuration`.

The SnapEngage Javascript code is inserted into templates using a
template tag.  Load the :mod:`SnapEngage` template tag library and
insert the :ttag:`SnapEngage` tag.  Because every page that you want to
track must have the tag, it is useful to add it to your base template.
Insert the tag at the bottom of the HTML body::

    {% load snapengage %}
    ...
    {% snapengage %}
    </body>
    </html>


.. _snapengage-configuration:

Configuration
=============

Before you can use the SnapEngage integration, you must first set the
widget ID.  You can customize the visitor nickname and add information
to their status in the operator buddy list, and customize the text used
in the chat window.


Setting the widget ID
---------------------

In order to install the chat code, you need to set the ID of the
SnapEngage widget.  You can find the site ID on the `Your Widget ID
page`_ of your SnapEngage account.  Set :const:`SNAPENGAGE_WIDGET_ID` in
the project :file:`settings.py` file::

    SNAPENGAGE_WIDGET_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

If you do not set the widget ID, the chat window will not be rendered.

.. _`Your Widget ID page`: https://secure.snapengage.com/getwidgetid


Customizing the widget
----------------------

The SnapEngage widget can be customized in various ways using either
context variables or settings.  More information about controlling the
widget can be found on the `customization FAQ section`_ of the
SnapEngage website.

=====================================  =====================================  ==================================================================
Setting                                Context variable                       Description
=====================================  =====================================  ==================================================================
``SNAPENGAGE_DOMAIN``                  ``snapengage_domain``                  Manually set the domain name to follow users across subdomains.
``SNAPENGAGE_SECURE_CONNECTION``       ``snapengage_secure_connection``       Force the use of SSL for the chat connection, even on unencrypted
                                                                              pages. (Default: ``False``)
``SNAPENGAGE_BUTTON_EFFECT``           ``snapengage_button_effect``           An effect applied when the mouse hovers over the button.
                                                                              (Example: ``"-4px"``)
``SNAPENGAGE_BUTTON_STYLE``            ``snapengage_button_style``            What the chat button should look like. Use any of the
                                                                              :const:`BUTTON_STYLE_*` constants, or a URL to a custom button
                                                                              image.
``SNAPENGAGE_BUTTON_LOCATION``         ``snapengage_button_location``         The location of the chat button. Use any of the
                                                                              :const:`BUTTON_LOCATION_*` constants.
``SNAPENGAGE_BUTTON_LOCATION_OFFSET``  ``snapengage_button_location_offset``  The offset of the button from the top or left side of the page.
                                                                              (Default: ``"55%"``)
``SNAPENGAGE_FORM_POSITION``           ``snapengage_form_position``           Configure the location of the chat window. Use any of the
                                                                              :const:`FORM_POSITION_*` constants.
``SNAPENGAGE_FORM_TOP_POSITION``       ``snapengage_form_top_position``       The chat window offset in pixels from the top of the page.
``SNAPENGAGE_READONLY_EMAIL``          ``snapengage_readonly_email``          Whether a preset e-mail address can be changed by the visitor.
                                                                              (Default: ``False``)
``SNAPENGAGE_SHOW_OFFLINE``            ``snapengage_show_offline``            Whether to show the chat button when all operators are offline.
                                                                              (Default: ``True``)
``SNAPENGAGE_SCREENSHOTS``             ``snapengage_screenshots``             Whether to allow the user to take a screenshot.
                                                                              (Default: ``True``)
``SNAPENGAGE_OFFLINE_SCREENSHOTS``     ``snapengage_offline_screenshots``     Whether to allow the user to take a screenshot when all operators
                                                                              are offline. (Default: ``True``)
``SNAPENGAGE_SOUNDS``                  ``snapengage_sounds``                  Whether to play chat sound notifications. (Default: ``True``)
=====================================  =====================================  ==================================================================

There are also two customizations that can only be used with context
variables.

=============================  =========================================
Context variable               Description
=============================  =========================================
``snapengage_proactive_chat``  Set to ``False`` to disable proactive
                               chat, for example for users who are
                               already converted.
``snapengage_email``           Set the e-mail address of the website
                               visitor. (See :ref:`snapengage-email`)
=============================  =========================================


.. _`customization FAQ section`: http://www.snapengage.com/faq#customization


.. _snapengage-email:

Setting the visitor e-mail address
----------------------------------

If your website identifies visitors, you can use that to pass their e-mail
address to the support agent.  By default, the e-mail address of an
authenticated user is automatically used.  See :ref:`identifying-visitors`.

You can also set the visitor e-mail address yourself by adding either the
``snapengage_email`` (alias: ``snapengage_identity``) or the
``analytical_identity`` variable to the template context.  If both
variables are set, the former takes precedence. For example::

    context = RequestContext({'snapengage_email': email})
    return some_template.render(context)

If you can derive the e-mail address from the HTTP request, you can also use
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    from django.core.exceptions import ObjectDoesNotExist

    def set_snapengage_email(request):
        try:
            profile = request.user.get_profile()
            return {'snapengage_email': profile.business_email}
        except (AttributeError, ObjectDoesNotExist):
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

If the user should not be able to edit the pre-set e-mail address, you
can set either the ``snapengage_readonly_email`` context variable or the
:setting:`SNAPENGAGE_READONLY_EMAIL` setting to ``True``.

----

Thanks go to SnapEngage for their support with the development of this
application.

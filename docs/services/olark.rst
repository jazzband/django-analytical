=====================
Olark -- visitor chat
=====================

Olark_ is a lightweight tool to chat with visitors to your website using
your existing instant messaging client.  Chat with your website visitors
while they browse, using your mobile device or instant messenger.  Olark
is fully customizable, supports multiple operators and keeps chat
transcripts.

.. _Olark: http://www.olark.com/


Installation
============

To start using the Olark integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Olark template tag to your templates.  This
step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`olark-configuration`.

The Olark Javascript code is inserted into templates using a template
tag.  Load the :mod:`olark` template tag library and insert the
:ttag:`olark` tag.  Because every page that you want to track
must have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body::

    {% load olark %}
    ...
    {% olark %}
    </body>
    </html>


.. _olark-configuration:

Configuration
=============

Before you can use the Olark integration, you must first set your site
ID.  You can also customize the visitor nickname and add information to
their status in the operator buddy list.


Setting the site ID
-------------------

In order to install the chat code, you need to set your Olark site ID.
The :ttag:`olark` tag will include it in the rendered Javascript code.
You can find the site ID on `installation page`_ of you Olark account.
Set :const:`OLARK_SITE_ID` in the project :file:`settings.py` file::

    OLARK_SITE_ID = 'XXXX-XXX-XX-XXXX'

If you do not set the site ID, the chat window will not be rendered.

.. _`installation page`: https://www.olark.com/install


Setting the visitor nickname
----------------------------

If your websites identifies visitors, you can use that to set their
nickname in the operator buddy list. By default, the name and username
of an authenticated user are automatically used to set the nickname.
See :ref:`identifying-visitors`.

You can also set the visitor nickname yourself by adding either the
``olark_nickname`` (alias: ``olark_identity``) or the
``analytical_identity`` variable to the template context.  If both
variables are set, the former takes precedence. For example::

    context = RequestContext({'olark_nickname': nick})
    return some_template.render(context)

If you can derive the identity from the HTTP request, you can also use
a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def set_olark_nickname(request):
        try:
            return {'olark_nickname': request.user.email}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

See also `api.chat.updateVisitorNickname`_ in the Olark Javascript API
documentation.

.. _`api.chat.updateVisitorNickname`: http://www.olark.com/documentation/javascript/api.chat.updateVisitorNickname


Adding status information
-------------------------

If you want to send more information about the visitor to the operators,
you can add text snippets to the status field in the buddy list.  Set
the ``olark_status`` context variable to a string or a list of strings
and the :ttag:`olark` tag will pass them to Olark as status messages::

    context = RequestContext({'olark_status': [
        'has %d items in cart' % cart.item_count,
        'value of items is $%0.2f' % cart.total_value,
    ]})
    return some_template.render(context)

See also `api.chat.updateVisitorStatus`_ in the Olark Javascript API
documentation.

.. _`api.chat.updateVisitorStatus`: http://www.olark.com/documentation/javascript/api.chat.updateVisitorStatus

----

Thanks go to Olark for their support with the development of this
application.

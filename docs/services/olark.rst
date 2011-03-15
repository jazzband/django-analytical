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
ID.  You can customize the visitor nickname and add information to their
status in the operator buddy list, and customize the text used in the
chat window.


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

If your website identifies visitors, you can use that to set their
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


Customizing the chat window messages
------------------------------------

Olark lets you customize the appearance of the Chat window by changing
location, colors and messages text.  While you can configure these on
the Olark website, sometimes one set of messages is not enough.  For
example, if you want to localize your website, you want to address every
visitor in their own language.  Olark allows you to set the messages on
a per-page basis, and the :ttag:`olark` tag supports this feature by way
of the following context variables:

========================================== =============================
Context variable                           Example message
========================================== =============================
``olark_welcome_title``                    Click to Chat
------------------------------------------ -----------------------------
``olark_chatting_title``                   Live Help: Now Chatting
------------------------------------------ -----------------------------
``olark_unavailable_title``                Live Help: Offline
------------------------------------------ -----------------------------
``olark_busy_title``                       Live Help: Busy
------------------------------------------ -----------------------------
``olark_away_message``                     Our live support feature is
                                           currently offline, Please
                                           try again later.
------------------------------------------ -----------------------------
``olark_loading_title``                    Loading Olark...
------------------------------------------ -----------------------------
``olark_welcome_message``                  Welcome to my website.  You
                                           can use this chat window to
                                           chat with me.
------------------------------------------ -----------------------------
``olark_busy_message``                     All of our representatives
                                           are with other customers at
                                           this time. We will be with
                                           you shortly.
------------------------------------------ -----------------------------
``olark_chat_input_text``                  Type here and hit  to chat
------------------------------------------ -----------------------------
``olark_name_input_text``                  and type your Name
------------------------------------------ -----------------------------
``olark_email_input_text``                 and type your Email
------------------------------------------ -----------------------------
``olark_offline_note_message``             We are offline, send us a
                                           message
------------------------------------------ -----------------------------
``olark_send_button_text``                 Send
------------------------------------------ -----------------------------
``olark_offline_note_thankyou_text``       Thank you for your message.
                                           We will get back to you as
                                           soon as we can.
------------------------------------------ -----------------------------
``olark_offline_note_error_text``          You must complete all fields
                                           and specify a valid email
                                           address
------------------------------------------ -----------------------------
``olark_offline_note_sending_text``        Sending...
------------------------------------------ -----------------------------
``olark_operator_is_typing_text``          is typing...
------------------------------------------ -----------------------------
``olark_operator_has_stopped_typing_text`` has stopped typing
------------------------------------------ -----------------------------
``olark_introduction_error_text``          Please leave a name and email
                                           address so we can contact you
                                           in case we get disconnected
------------------------------------------ -----------------------------
``olark_introduction_messages``            Welcome, just fill out some
                                           brief information and click
                                           'Start chat' to talk to us
------------------------------------------ -----------------------------
``olark_introduction_submit_button_text``  Start chat
========================================== =============================

As an example, you could set the texts site-wide base on the current
language using a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    OLARK_TEXTS = {
        'en': {
            'welcome title':  "Click for Live Help",
            'chatting_title': "Live Help: Now chatting",
            ...
        },
        'nl': {
            'welcome title':  "Klik voor online hulp",
            'chatting_title': "Online hulp: in gesprek",
            ...
        },
        ...
    }

    def set_olark_texts(request):
        lang = request.LANGUAGE_CODE.split('-', 1)[0]
        texts = OLARK_TEXTS.get(lang)
        if texts is None:
            texts = OLARK_TEXTS.get('en')
        return dict(('olark_%s' % k, v) for k, v in texts.items())


See also the Olark blog post on `supporting multiple languages`_.

.. _`supporting multiple languages`: http://www.olark.com/blog/2010/olark-in-your-favorite-language/


----

Thanks go to Olark for their support with the development of this
application.

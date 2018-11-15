=================================
Intercom.io -- Real-time tracking
=================================

Intercom.io_ is an easy way to implement real-chat and individual
support for a website

.. _Intercom.io: http://www.intercom.io/


.. intercom-installation:

Installation
============

To start using the Intercom.io integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Intercom.io template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`intercom-configuration`.

The Intercom.io Javascript code is inserted into templates using a
template tag.  Load the :mod:`intercom` template tag library and
insert the :ttag:`intercom` tag.  Because every page that you want to
track must have the tag, it is useful to add it to your base template.
Insert the tag at the bottom of the HTML body::

    {% load intercom %}
    <html>
    <head></head>
    <body>
    <!-- Your page -->
    {% intercom %}
    </body>
    </html>
    ...


.. _intercom-configuration:

Configuration
=============

Before you can use the Intercom.io integration, you must first set your
app id.


.. _intercom-site-id:

Setting the app id
--------------------------

Intercom.io gives you a unique app id, and the :ttag:`intercom`
tag will include it in the rendered Javascript code.  You can find your
app id by clicking the *Tracking Code* link when logged into
the on the intercom.io website.  A page will display containing
HTML code looking like this::

    <script id="IntercomSettingsScriptTag">
        window.intercomSettings = { name: "Jill Doe", email: "jill@example.com", created_at: 1234567890, app_id: "XXXXXXXXXXXXXXXXXXXXXXX" };
    </script>
    <script>(function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',intercomSettings);}else{var d=document;var i=function(){i.c(arguments)};i.q=[];i.c=function(args){i.q.push(args)};w.Intercom=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://static.intercomcdn.com/intercom.v1.js';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}}})()</script>

The code ``XXXXXXXXXXXXXXXXXXXXXXX`` is your app id.  Set
:const:`INTERCOM_APP_ID` in the project :file:`settings.py`
file::

    INTERCOM_APP_ID = 'XXXXXXXXXXXXXXXXXXXXXXX'

If you do not set an app id, the Javascript code will not be
rendered.


Custom data
-----------

As described in the Intercom documentation on `custom visitor data`_,
the data that is tracked by Intercom can be customized.  Using template
context variables, you can let the :ttag:`intercom` tag pass custom data
to Intercom automatically.  You can set the context variables in your view
when your render a template containing the tracking code::

    context = RequestContext({'intercom_cart_value': cart.total_price})
    return some_template.render(context)

For some data, it is annoying to do this for every view, so you may want
to set variables in a context processor that you add to the
:data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    from django.utils.hashcompat import md5_constructor as md5

    GRAVATAR_URL = 'http://www.gravatar.com/avatar/'

    def intercom_custom_data(request):
        try:
            email = request.user.email
        except AttributeError:
            return {}
        email_hash = md5(email).hexdigest()
        avatar_url = "%s%s" % (GRAVATAR_URL, email_hash)
        return {'intercom_avatar': avatar_url}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

Standard variables that will be displayed in the Intercom live visitor
data are listed in the table below, but you can define any ``intercom_*``
variable you like and have that detail passed from within the visitor
live stream data when viewing Intercom.

====================  ===========================================
Context variable       Description
====================  ===========================================
``intercom_name``       The visitor's full name.
--------------------  -------------------------------------------
``intercom_email``      The visitor's email address.
--------------------  -------------------------------------------
``intercom_user_id``    The visitor's user id.
--------------------  -------------------------------------------
``created_at``          The date the visitor created an account
====================  ===========================================


.. _`custom visitor data`: https://www.intercom.com/help/configure-intercom-for-your-product-or-site/customize-intercom-to-be-about-your-users/send-custom-user-attributes-to-intercom


Identifying authenticated users
-------------------------------

If you have not set the ``intercom_name``, ``intercom_email``, or ``intercom_user_id`` variables
explicitly, the username and email address of an authenticated user are
passed to Intercom automatically.  See :ref:`identifying-visitors`.

.. _intercom-internal-ips:


Verifying identified users
--------------------------

Intercom supports HMAC authentication of users identified by user ID or email, in order to prevent impersonation.
For more information, see `Enable identity verification on your web product`_ in the Intercom documentation.

To enable this, configure your Intercom account's HMAC secret key::

    INTERCOM_HMAC_SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'

(You can find this secret key under the "Identity verification" section of your Intercom account settings page.)

.. _`Enable identity verification on your web product`: https://www.intercom.com/help/configure-intercom-for-your-product-or-site/staying-secure/enable-identity-verification-on-your-web-product



Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`ANALYTICAL_INTERNAL_IPS` setting
(which is :const:`INTERNAL_IPS` by default,) the tracking code is 
commented out. See :ref:`identifying-visitors` for important information
about detecting the visitor IP address.

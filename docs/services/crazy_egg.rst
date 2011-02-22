==================================
Crazy Egg -- visual click tracking
==================================

`Crazy Egg`_ is an easy to use hosted web application that visualizes
website clicks using heatmaps.  It allows you to discover the areas of
web pages that are most important to your visitors.

.. _`Crazy Egg`: http://www.crazyegg.com/


.. crazy-egg-installation:

Installation
============

To start using the Crazy Egg integration, you must have installed the
django-analytical package and have added the ``analytical`` application
to :const:`INSTALLED_APPS` in your project :file:`settings.py` file.
See :doc:`../install` for details.

Next you need to add the Crazy Egg template tag to your templates.
This step is only needed if you are not using the generic
:ttag:`analytical.*` tags.  If you are, skip to
:ref:`crazy-egg-configuration`.

The Crazy Egg tracking code is inserted into templates using a template
tag.  Load the :mod:`crazy_egg` template tag library and insert the
:ttag:`crazy_egg` tag.  Because every page that you want to track must
have the tag, it is useful to add it to your base template.  Insert
the tag at the bottom of the HTML body::

    {% load crazy_egg %}
    ...
    {% crazy_egg %}
    </body>
    </html>


.. _crazy-egg-configuration:

Configuration
=============

Before you can use the Crazy Egg integration, you must first set your
account number.  You can also segment the click analysis through user
variables.


.. _crazy-egg-account-number:

Setting the account number
--------------------------

Crazy Egg gives you a unique account number, and the :ttag:`crazy egg`
tag will include it in the rendered Javascript code. You can find your
account number by clicking the link named "What's my code?" in the
dashboard of your Crazy Egg account.  Set
:const:`CRAZY_EGG_ACCOUNT_NUMBER` in the project :file:`settings.py`
file::

    CRAZY_EGG_ACCOUNT_NUMBER = 'XXXXXXXX'

If you do not set an account number, the tracking code will not be
rendered.


.. _crazy-egg-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`CRAZY_EGG_INTERNAL_IPS` setting,
the tracking code is commented out.  It takes the value of
:const:`ANALYTICAL_INTERNAL_IPS` by default (which in turn is
:const:`INTERNAL_IPS` by default).  See :ref:`identifying-visitors` for
important information about detecting the visitor IP address.


.. _crazy-egg-uservars:

User variables
--------------

Crazy Egg can segment clicks based on `user variables`_.  If you want to
set a user variable, use the context variables ``crazy_egg_var1``
through ``crazy_egg_var5`` when you render your template::

    context = RequestContext({'crazy_egg_var1': 'red',
                              'crazy_egg_var2': 'male'})
    return some_template.render(context)

If you use the same user variables in different views and its value can
be computed from the HTTP request, you can also set them in a context
processor that you add to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list
in :file:`settings.py`::

    def track_admin_role(request):
        if request.user.is_staff():
            role = 'staff'
        else:
            role = 'visitor'
        return {'crazy_egg_var3': role}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

.. _`user variables`: https://www.crazyegg.com/help/Setting_Up_A_Page_to_Track/How_do_I_set_the_values_of_User_Var_1_User_Var_2_etc_in_the_confetti_and_overlay_views/


----

The work on Crazy Egg was made possible by `Bateau Knowledge`_. Thanks
go to Crazy Egg for their support with the development of this
application.

.. _`Bateau Knowledge`: http://www.bateauknowledge.nl/

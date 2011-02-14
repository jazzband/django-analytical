==========================
Geckoboard -- status board
==========================

Geckoboard_ is a hosted, real-time status board serving up indicators
from web analytics, CRM, support, infrastructure, project management,
sales, etc.  It can be connected to virtually any source of quantitative
data.

.. _Geckoboard: https://www.geckoboard.com/


.. _geckoboard-installation:

Installation
============

Geckoboard works differently from most other analytics services in that
it pulls measurement data from your website periodically.  You will not
have to change anything in your existing templates, and there is no need
to install the ``analytical`` application to use the integration.
Instead you will use custom views to serve the data to Geckoboard custom
widgets.


.. _geckoboard-configuration:

Configuration
=============

If you want to protect the data you send to Geckoboard from access by
others, you can use an API key shared by Geckoboard and your widget
views.  Set :const:`GECKOBOARD_API_KEY` in the project
:file:`settings.py` file::

    GECKOBOARD_API_KEY = 'XXXXXXXXX'

Provide the API key to the custom widget configuration in Geckoboard.
If you do not set an API key, anyone will be able to view the data by
visiting the widget URL.


Creating custom widgets and charts
==================================

The available custom widgets are described in the Geckoboard support
section, under `Geckoboard API`_.  From the perspective of a Django
project, a custom widget is just a view.  The django-analytical
application provides view decorators that render the correct response
for the different widgets.  When you create a custom widget, enter the
following information:

URL data feed
    The view URL.

API key
    The content of the :const:`GECKOBOARD_API_KEY` setting, if you have
    set it.

Widget type
    *Custom*

Feed format
    Either *XML* or *JSON*.  The view decorators will automatically
    detect and output the correct format.

Request type
    Either *GET* or *POST*.  The view decorators accept both.

Then create a view using one of the decorators from the
:mod:`analytical.geckoboard` module.

.. decorator:: number

    Render a *Number & Secondary Stat* widget.

    The decorated view must return either a single value, or a list or
    tuple with one or two values.  The first (or only) value represents
    the current value, the second value represents the previous value.
    For example, to render a widget that shows the number of active
    users and the difference from last week::

        from analytical import geckoboard
        from datetime import datetime, timedelta
        from django.contrib.auth.models import User

        @geckoboard.number
        def user_count(request):
            last_week = datetime.now() - timedelta(weeks=1)
            users = User.objects.filter(is_active=True)
            last_week_users = users.filter(date_joined__lt=last_week)
            return (users.count(), last_week_users.count())


.. decorator:: rag

    Render a *RAG Column & Numbers* or *RAG Numbers* widget.

    The decorated view must return a tuple or list with three values, or
    three tuples (value, text).  The values represent numbers shown in
    red, amber and green respectively.  The text parameter is optional
    and will be displayed next to the value in the dashboard.  For
    example, to render a widget that shows the number of comments that
    were approved or deleted by moderators in the last 24 hours::

        from analytical import geckoboard
        from datetime import datetime, timedelta
        from django.contrib.comments.models import Comment, CommentFlag

        @geckoboard.rag
        def comments(request):
            start_time = datetime.now() - timedelta(hours=24)
            comments = Comment.objects.filter(submit_date__gt=start_time)
            total_count = comments.count()
            approved_count = comments.filter(
                    flags__flag=CommentFlag.MODERATOR_APPROVAL).count()
            deleted_count = Comment.objects.filter(
                    flags__flag=CommentFlag.MODERATOR_DELETION).count()
            pending_count = total_count - approved_count - deleted_count
            return (
                (deleted_count, "Deleted comments"),
                (pending_count, "Pending comments"),
                (approved_count, "Approved comments"),
            )


.. decorator:: text

    Render a *Text* widget.

    The decorated view must return either a string, a list or tuple of
    strings, or a list or tuple of tuples (string, type).  The type
    parameter tells Geckoboard how to display the text.  Use
    :const:`TEXT_INFO` for informational messages, :const:`TEXT_WARN`
    for warnings and :const:`TEXT_NONE` for plain text (the default).
    For example, to render a widget showing the latest Geckoboard
    twitter updates::

        from analytical import geckoboard
        import twitter

        @geckoboard.text
        def twitter_status(request):
            twitter = twitter.Api()
            updates = twitter.GetUserTimeline('geckoboard')
            return [(u.text, geckoboard.TEXT_NONE) for u in updates]



.. decorator:: pie_chart

    Render a *Pie chart* widget.

    The decorated view must return a list or tuple of tuples
    (value, label, color).  The color parameter is a string
    ``'RRGGBB[TT]'`` representing red, green, blue and optionally
    transparency.  For example, to render a widget showing the number
    of normal, staff and superusers::

        from analytical import geckoboard
        from django.contrib.auth.models import User

        @geckoboard.pie_chart
        def user_types(request):
            users = User.objects.filter(is_active=True)
            total_count = users.count()
            superuser_count = users.filter(is_superuser=True).count()
            staff_count = users.filter(is_staff=True,
                                       is_superuser=False).count()
            normal_count = total_count = superuser_count - staff_count
            return [
                (normal_count,    "Normal users", "ff8800"),
                (staff_count,     "Staff",        "00ff88"),
                (superuser_count, "Superusers",   "8800ff"),
            ]


.. decorator:: line_chart

    Render a *Line chart* widget.

    The decorated view must return a tuple (values, x_axis, y_axis,
    color).  The value parameter is a tuple or list of data points.  The
    x-axis parameter is a label string, or a tuple or list of strings,
    that will be placed on the X-axis.  The y-axis parameter works
    similarly for the Y-axis.  If there are more axis labels, they are
    placed evenly along the axis.  The optional color parameter is a
    string ``'RRGGBB[TT]'`` representing red, green, blue and optionally
    transparency.  For example, to render a widget showing the number
    of comments per day over the last four weeks (including today)::

        from analytical import geckoboard
        from datetime import date, timedelta
        from django.contrib.comments.models import Comment

        @geckoboard.line_chart
        def comment_trend(request):
            since = date.today() - timedelta(days=29)
            days = dict((since + timedelta(days=d), 0)
                    for d in range(0, 29))
            comments = Comment.objects.filter(submit_date=since)
            for comment in comments:
                days[comment.submit_date.date()] += 1
            return (
                days.values(),
                [days[i] for i in range(0, 29, 7)],
                "Comments",
            )


.. decorator:: geck_o_meter

    Render a *Geck-O-Meter* widget.

    The decorated view must return a tuple (value, min, max).  The value
    parameter represents the current value.  The min and max parameters
    represent the minimum and maximum value respectively.  They are
    either a value, or a tuple (value, text).  If used, the text
    parameter will be displayed next to the minimum or maximum value.
    For example, to render a widget showing the number of users that
    have logged in in the last 24 hours::

        from analytical import geckoboard
        from datetime import datetime, timedelta
        from django.contrib.auth.models import User

        @geckoboard.geck_o_meter
        def login_count(request):
            since = datetime.now() - timedelta(hours=24)
            users = User.objects.filter(is_active=True)
            total_count = users.count()
            logged_in_count = users.filter(last_login__gt=since).count()
            return (logged_in_count, 0, total_count)


.. _`Geckoboard API`: http://geckoboard.zendesk.com/forums/207979-geckoboard-api


----

Thanks go to Geckoboard for their support with the development of this
application.

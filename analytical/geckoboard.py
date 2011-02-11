"""
Geckoboard decorators.
"""

import base64
from xml.dom.minidom import Document

try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import SortedDict
from django.utils.decorators import available_attrs
from django.utils import simplejson


TEXT_NONE = 0
TEXT_INFO = 2
TEXT_WARN = 1


class WidgetDecorator(object):
    """
    Geckoboard widget decorator.

    The decorated view must return a data structure suitable for
    serialization to XML or JSON for Geckoboard.  See the Geckoboard
    API docs or the source of extending classes for details.

    If the GECKOBOARD_API_KEY setting is used, the request must contain
    the correct API key, or a 403 Forbidden response is returned.
    """
    def __call__(self, view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not _is_api_key_correct(request):
                return HttpResponseForbidden("Geckoboard API key incorrect")
            view_result = view_func(request, *args, **kwargs)
            data = self._convert_view_result(view_result)
            content = _render(request, data)
            return HttpResponse(content)
        wrapper = wraps(view_func, assigned=available_attrs(view_func))
        return wrapper(_wrapped_view)

    def _convert_view_result(self, data):
        # Extending classes do view result mangling here.
        return data

widget = WidgetDecorator()


class NumberWidgetDecorator(WidgetDecorator):
    """
    Geckoboard number widget decorator.

    The decorated view must return either a single value, or a list or
    tuple with one or two values.  The first (or only) value represents
    the current value, the second value represents the previous value.
    """

    def _convert_view_result(self, result):
        if not isinstance(result, (tuple, list)):
            result = [result]
        return {'item': [{'value': v} for v in result]}

number = NumberWidgetDecorator()


class RAGWidgetDecorator(WidgetDecorator):
    """
    Geckoboard red-amber-green widget decorator.

    The decorated view must return a tuple or list with three values,
    or three tuples (value, text).  The values represent numbers shown
    in red, amber and green respectively.  The text parameter is
    optional and will be displayed next to the value in the dashboard.
    """

    def _convert_view_result(self, result):
        data = {'item': []}
        for elem in result:
            if not isinstance(elem, (tuple, list)):
                elem = [elem]
            item = {}
            if elem[0] is None:
                item['value'] = ''
            else:
                item['value'] = elem[0]
            if len(elem) > 1:
                item['text'] = elem[1]
            data.append(item)
        return data

rag = RAGWidgetDecorator()


class TextWidgetDecorator(WidgetDecorator):
    """
    Geckoboard text widget decorator.

    The decorated view must return a list or tuple of strings, or tuples
    (string, type).  The type parameter tells Geckoboard how to display
    the text.  Use TEXT_INFO for informational messages, TEXT_WARN for
    warnings and TEXT_NONE for plain text (the default).
    """

    def _convert_view_result(self, result):
        data = {'item': []}
        for elem in result:
            if not isinstance(elem, (tuple, list)):
                elem = [elem]
            item = {}
            item['text'] = elem[0]
            if len(elem) > 1:
                item['type'] = elem[1]
            else:
                item['type'] = TEXT_NONE
            data.append(item)
        return data

text = TextWidgetDecorator()


class PieChartWidgetDecorator(WidgetDecorator):
    """
    Geckoboard pie chart widget decorator.

    The decorated view must return a list or tuple of tuples
    (value, label, color).  The color parameter is a string 'RRGGBB[TT]'
    representing red, green, blue and optionally transparency.
    """

    def _convert_view_result(self, result):
        data = {'item': []}
        for elem in result:
            if not isinstance(elem, (tuple, list)):
                elem = [elem]
            item = {}
            item['value'] = elem[0]
            if len(elem) > 1:
                item['label'] = elem[1]
            if len(elem) > 2:
                item['colour'] = elem[2]
            data.append(item)
        return data

pie_chart = PieChartWidgetDecorator()


class LineChartWidgetDecorator(WidgetDecorator):
    """
    Geckoboard line chart widget decorator.

    The decorated view must return a tuple (values, x_axis, y_axis,
    color).  The value parameter is a tuple or list of data points.  The
    x-axis parameter is a label string, or a tuple or list of strings,
    that will be placed on the X-axis.  The y-axis parameter works
    similarly for the Y-axis.  If there are more axis labels, they are
    placed evenly along the axis.  The color parameter is a string
    'RRGGBB[TT]' representing red, green, blue and optionally
    transparency.
    """

    def _convert_view_result(self, result):
        data = {'item': result[0], 'settings': {}}

        x_axis = result[1]
        if x_axis in None:
            x_axis = ''
        if not isinstance(x_axis, (tuple, list)):
            x_axis = [x_axis]
        data['settings']['axisx'] = x_axis

        y_axis = result[2]
        if y_axis in None:
            y_axis = ''
        if not isinstance(y_axis, (tuple, list)):
            y_axis = [y_axis]
        data['settings']['axisy'] = y_axis

        if len(result) > 3 and result[3] is not None:
            data['settings']['colour'] = result[3]

        return data

line_chart = LineChartWidgetDecorator()


class GeckOMeterWidgetDecorator(WidgetDecorator):
    """
    Geckoboard Geck-O-Meter widget decorator.

    The decorated view must return a tuple (value, min, max).  The value
    parameter represents the current value.  The min and max parameters
    represent the minimum and maximum value respectively.  They are
    either a value, or a tuple (value, text).  If used, the text
    parameter will be displayed next to the minimum or maximum value.
    """

    def _convert_view_result(self, result):
        value, min, max = result
        data = {'item': value}

        if isinstance(min, (tuple, list)):
            min = [min]
        min_data = {'value': min[0]}
        if len(min) > 1:
            min_data['text'] = min[1]
        data['min'] = min_data

        if isinstance(max, (tuple, list)):
            max = [max]
        max_data = {'value': max[0]}
        if len(max) > 1:
            max_data['text'] = max[1]
        data['max'] = max_data

        return data

geck_o_meter = GeckOMeterWidgetDecorator()


def _is_api_key_correct(request):
    """Return whether the Geckoboard API key on the request is correct."""
    api_key = getattr(settings, 'GECKOBOARD_API_KEY', None)
    if api_key is None:
        return True
    auth = request.META.get('HTTP_AUTHORIZATION', '').split()
    if len(auth) == 2:
        if auth[0].lower() == 'basic':
            request_key = base64.b64decode(auth[1])
            return request_key == api_key
    return False


def _render(request, data):
    if request.POST.get('format') == '2':
        return _render_json(data)
    else:
        return _render_xml(data)

def _render_json(data):
    return simplejson.dumps(data)

def _render_xml(data):
    doc = Document()
    root = doc.createElement('root')
    doc.appendChild(root)
    _build_xml(doc, root, data)
    return doc.toxml()

def _build_xml(doc, parent, data):
    func = _build_xml_vtable.get(type(data), _build_str_xml)
    func(doc, parent, data)

def _build_str_xml(doc, parent, data):
    parent.appendChild(doc.createTextNode(str(data)))

def _build_list_xml(doc, parent, data):
    for item in data:
        _build_xml(doc, parent, item)

def _build_dict_xml(doc, parent, data):
    for tag, item in data.items():
        if isinstance(item, (list, tuple)):
            for subitem in item:
                elem = doc.createElement(tag)
                _build_xml(doc, elem, subitem)
                parent.appendChild(elem)
        else:
            elem = doc.createElement(tag)
            _build_xml(doc, elem, item)
            parent.appendChild(elem)

_build_xml_vtable = {
    list:  _build_list_xml,
    tuple: _build_list_xml,
    dict:  _build_dict_xml,
}

_render_vtable = {
    '1': _render_xml,
    '2': _render_json,
}


class GeckoboardException(Exception):
    """
    Represents an error with the Geckoboard decorators.
    """

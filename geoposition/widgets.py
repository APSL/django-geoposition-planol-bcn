from __future__ import unicode_literals

import json
from django import forms
from django.template.loader import render_to_string
import six
from django.utils.translation import ugettext_lazy as _

from geoposition import constants
from .conf import settings

import json
import sys

from django import forms
from django.utils.translation import ugettext_lazy as _

from .conf import settings


PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
else:
    text_type = str


class GeopositionWidget(forms.MultiWidget):
    template_name = 'geoposition/widgets/geoposition.html'

    backends = {
        'google': {
            'js': (
                '//maps.google.com/maps/api/js?key=%s' % settings.GOOGLE_MAPS_API_KEY,
                'geoposition/google.js',
            ),
            'css': (),
        },
        'bcn': {
            'js': (
                'geoposition/geoposition_planol_bcn.js',
                'https://www.barcelona.cat/api-management/javascripts/geobcn.min.js',
                'https://www.barcelona.cat/api-service/bcn-planol/js/bcn_service_planol.min.js'
            ),
            'css': (),
        }
    }

    def __init__(self, attrs=None):
        self.Media.js = self.backends['bcn']['js']
        self.Media.css['all'] = self.backends['bcn']['css'] + self.Media.css['all']
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def get_config(self):
        return {
            'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
            'map_options': json.dumps(settings.MAP_OPTIONS),
            'marker_options': json.dumps(settings.MARKER_OPTIONS),
        }

    def get_context(self, name, value, attrs):
        context = super(GeopositionWidget, self).get_context(name, value, attrs)
        if not isinstance(value, list):
            value = self.decompress(value)
        if 'widget' not in context:
            context['widget'] = {}
        context['widget'].update({
            'latitude': {
                'html': value[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': value[1],
                'label': _("longitude"),
            },
            'config': {
                'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
                'map_options': json.dumps(settings.MAP_OPTIONS),
                'marker_options': json.dumps(settings.MARKER_OPTIONS),
                'api_key': settings.PLANOL_BCN_MAPS_API_KEY or None,
            }
        })
        return context

    def decompress(self, value):
        if isinstance(value, text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return ['', '']

    class Media:
        css = {
            'all': ('geoposition/geoposition.css',)
        }


# class GeopositionWidget(forms.MultiWidget):
#     def __init__(self, attrs=None):
#         widgets = (
#             forms.TextInput(),
#             forms.TextInput(),
#         )
#         super(GeopositionWidget2, self).__init__(widgets, attrs)
#
#     def decompress(self, value):
#         if isinstance(value, six.text_type):
#             return value.rsplit(',')
#         if value:
#             return [value.latitude, value.longitude]
#         return [None, None]
#
#     def format_output(self, rendered_widgets):
#         return render_to_string('geoposition/widgets/geoposition.html', {
#             'latitude': {
#                 'html': rendered_widgets[0],
#                 'label': _("latitude"),
#             },
#             'longitude': {
#                 'html': rendered_widgets[1],
#                 'label': _("longitude"),
#             },
#             'config': {
#                 'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
#                 'map_options': json.dumps(settings.MAP_OPTIONS),
#                 'marker_options': json.dumps(settings.MARKER_OPTIONS),
#                 'api_key': settings.PLANOL_BCN_MAPS_API_KEY or None,
#             }
#         })
#
#     class Media:
#         if settings.ENGINE_APY_KEY == constants.GOOGLE_MAPS:
#             js = (
#                 '//maps.google.com/maps/api/js?key=%s' % settings.GOOGLE_MAPS_API_KEY,
#                 'geoposition/geoposition.js',
#             )
#         else:
#             js = (
#                 'geoposition/geoposition_planol_bcn.js',
#                 'https://www.barcelona.cat/api-management/javascripts/geobcn.min.js',
#                 'https://www.barcelona.cat/api-service/bcn-planol/js/bcn_service_planol.min.js'
#             )
#         css = {
#             'all': ('geoposition/geoposition.css',)
#         }

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import (MaternalArvPregForm, MaternalArvPregHistoryForm, MaternalArvPPHistoryForm,
                     MaternalArvForm)
from ..models import MaternalArvPreg, MaternalArvPregHistory, MaternalArvPPHistory, MaternalArv
from .site import admin_site


class MaternalArvPregAdmin(BaseModelAdmin):
    form = MaternalArvPregForm
    list_display = ('took_arv', 'sd_nvp', 'start_pp')
    list_filter = ('took_arv', 'start_pp')
    radio_fields = {'took_arv':admin.VERTICAL,
                    'sd_nvp':admin.VERTICAL,
                    'start_pp':admin.VERTICAL, }
admin_site.register(MaternalArvPreg, MaternalArvPregAdmin)


class MaternalArvPregHistoryAdmin(BaseModelAdmin):
    form = MaternalArvPregHistoryForm
    list_display = ('is_interrupt', )
    radio_fields = {'is_interrupt':admin.VERTICAL, }
admin_site.register(MaternalArvPregHistory, MaternalArvPregHistoryAdmin)


class MaternalArvPPHistoryAdmin(BaseModelAdmin):
    form = MaternalArvPPHistoryForm
admin_site.register(MaternalArvPPHistory, MaternalArvPPHistoryAdmin)


class MaternalArvAdmin(BaseModelAdmin):
    form = MaternalArvForm
admin_site.register(MaternalArv, MaternalArvAdmin)

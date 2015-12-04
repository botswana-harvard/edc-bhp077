from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline

from ..forms import MaternalArvPregForm, MaternalArvForm
from ..models import MaternalArvPreg, MaternalArv

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalArvInlineAdmin(BaseTabularInline):
    model = MaternalArv
    form = MaternalArvForm
    extra = 1


class MaternalArvPregAdmin(BaseMaternalModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('arv_exposed',)
    list_filter = ('arv_exposed',)
    radio_fields = {'arv_exposed': admin.VERTICAL,
                    'interrupt': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL, }
admin.site.register(MaternalArvPreg, MaternalArvPregAdmin)


class MaternalArvAdmin(BaseMaternalModelAdmin):
    form = MaternalArvForm
admin.site.register(MaternalArv, MaternalArvAdmin)

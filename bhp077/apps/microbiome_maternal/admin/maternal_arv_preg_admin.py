from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalArvPregForm
from ..models import MaternalArvPreg, MaternalArv


class MaternalArvInlineAdmin(BaseTabularInline):
    model = MaternalArv
    extra = 1


class MaternalArvPregAdmin(BaseModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('took_arv', 'is_interrupt')
    list_filter = ('took_arv', 'is_interrupt')
    radio_fields = {'took_arv': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL}
admin.site.register(MaternalArvPreg, MaternalArvPregAdmin)

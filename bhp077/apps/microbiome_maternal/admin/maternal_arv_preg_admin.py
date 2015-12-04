from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline

from ..forms import MaternalArvPregForm, MaternalArvForm
from ..models import MaternalArvPreg, MaternalArv, MaternalVisit

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalArvInlineAdmin(BaseTabularInline):
    model = MaternalArv
    form = MaternalArvForm
    extra = 1


class MaternalArvPregAdmin(BaseMaternalModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('maternal_visit', 'took_arv',)
    list_filter = ('took_arv',)
    radio_fields = {'took_arv': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL,
                    'interrupt': admin.VERTICAL
                    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalArvPregAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvPreg, MaternalArvPregAdmin)


class MaternalArvAdmin(BaseMaternalModelAdmin):
    form = MaternalArvForm
admin.site.register(MaternalArv, MaternalArvAdmin)

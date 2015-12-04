from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalArvPregForm, MaternalArvForm
from ..models import MaternalArvPreg, MaternalArv, MaternalVisit


class MaternalArvInlineAdmin(BaseTabularInline):
    model = MaternalArv
    form = MaternalArvForm
    extra = 1


class MaternalArvPregAdmin(BaseModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('arv_exposed',)
    list_filter = ('arv_exposed',)
    radio_fields = {'arv_exposed': admin.VERTICAL,
                    'interrupt': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalArvPregAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvPreg, MaternalArvPregAdmin)


class MaternalArvAdmin(BaseModelAdmin):
    form = MaternalArvForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalArvAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArv, MaternalArvAdmin)

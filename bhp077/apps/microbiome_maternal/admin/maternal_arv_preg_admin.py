from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalArvPregForm
from ..models import MaternalArvPreg, MaternalArv, MaternalVisit


class MaternalArvInlineAdmin(BaseTabularInline):
    model = MaternalArv
    extra = 1


class MaternalArvPregAdmin(BaseModelAdmin):
    form = MaternalArvPregForm
    inlines = [MaternalArvInlineAdmin, ]
    list_display = ('took_arv',)
    list_filter = ('took_arv',)
    radio_fields = {'took_arv': admin.VERTICAL,
                    'interrupt': admin.VERTICAL,
                    'is_interrupt': admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalArvPregAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvPreg, MaternalArvPregAdmin)

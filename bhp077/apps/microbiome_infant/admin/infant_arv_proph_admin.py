from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import InfantArvProphMod, InfantArvProph, InfantVisit


class InfantArvProphAdmin(BaseModelAdmin):

    radio_fields = {
        'prophylatic_nvp': admin.VERTICAL,
        'arv_status': admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantArvProphAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantArvProph, InfantArvProphAdmin)


class InfantArvProphModAdmin(BaseModelAdmin):

    list_filter = ('infant_arv_proph',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantArvProphModAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantArvProphMod, InfantArvProphModAdmin)

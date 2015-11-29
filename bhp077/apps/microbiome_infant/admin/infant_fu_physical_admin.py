from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantFuPhysicalForm
from ..models import InfantVisit, InfantFuPhysical


class InfantFuPhysicalAdmin(BaseModelAdmin):
    form = InfantFuPhysicalForm

    list_display = ('has_abnormalities', )

    radio_fields = {'has_abnormalities': admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantFuPhysicalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFuPhysical, InfantFuPhysicalAdmin)

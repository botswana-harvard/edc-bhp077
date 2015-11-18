from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..forms import InfantFuImmunizationsForm
from ..models import InfantFuImmunizations, VaccinesReceived, VaccinesMissed, InfantVisit, InfantFu


class VaccinesReceivedInlineAdmin(BaseTabularInline):
    model = VaccinesReceived
    extra = 1


class VaccinesMissedInlineAdmin(BaseTabularInline):
    model = VaccinesMissed
    extra = 1


class InfantFuImmunizationsAdmin(BaseModelAdmin):
    form = InfantFuImmunizationsForm
    inlines = [VaccinesReceivedInlineAdmin, VaccinesMissedInlineAdmin, ]
    radio_fields = {'vaccines_received': admin.VERTICAL,
                    'vaccines_missed': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        if db_field.name == "infant_fu":
                infant_subject_identifier = InfantVisit.objects.get(id=request.GET.get('infant_visit')).appointment.registered_subject.subject_identifier
                kwargs["queryset"] = InfantFu.objects.filter(infant_visit__appointment__registered_subject__subject_identifier=infant_subject_identifier)
        return super(InfantFuImmunizationsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFuImmunizations, InfantFuImmunizationsAdmin)

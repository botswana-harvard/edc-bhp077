from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import InfantFuNewMed, InfantVisit, InfantFu


class InfantFuNewMedAdmin(BaseModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        if db_field.name == "infant_fu":
                infant_subject_identifier = InfantVisit.objects.get(id=request.GET.get('infant_visit')).appointment.registered_subject.subject_identifier
                kwargs["queryset"] = InfantFu.objects.filter(infant_visit__appointment__registered_subject__subject_identifier=infant_subject_identifier)
        return super(InfantFuNewMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFuNewMed, InfantFuNewMedAdmin)

from django.contrib import admin

from ..models import InfantFuImmunizations
from ..models import InfantFu, InfantVisit


class InfantFuImmunizationsAdmin(admin.ModelAdmin):

    list_display = ('vaccines_received', 'vitamin_a_vaccine', 'pneumonia_conjugated_vaccine')

    radio_fields = {
        'vaccines_received': admin.VERTICAL,
        'vitamin_a_vaccine': admin.VERTICAL,
        'reason_not_received_vita_a': admin.VERTICAL,
        'bcg_vaccine': admin.VERTICAL,
        'reason_not_received_bcg': admin.VERTICAL,
        'hepatitis_b_vaccine': admin.VERTICAL,
        'reason_not_received_hepatitis_b': admin.VERTICAL,
        'dpt_vaccine': admin.VERTICAL,
        'reason_not_received_dpt': admin.VERTICAL,
        'haemophilus_influenza_b_vaccine': admin.VERTICAL,
        'reason_not_received_haemophilus': admin.VERTICAL,
        'pneumonia_conjugated_vaccine': admin.VERTICAL,
        'reason_not_received_pcv': admin.VERTICAL,
        'polio_vaccine': admin.VERTICAL,
        'reason_not_received_polio': admin.VERTICAL,
        'rotavirus_vaccine': admin.VERTICAL,
        'reason_not_received_rotavirus': admin.VERTICAL,
        'measles_vaccine': admin.VERTICAL,
        'reason_not_received_measles': admin.VERTICAL,
        'pentavalent_vaccine': admin.VERTICAL,
        'reason_not_received_pentavalent': admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        if db_field.name == "infant_fu":
                infant_subject_identifier = InfantVisit.objects.get(id=request.GET.get('infant_visit')).appointment.registered_subject.subject_identifier
                kwargs["queryset"] = InfantFu.objects.filter(infant_visit__appointment__registered_subject__subject_identifier=infant_subject_identifier)
        return super(InfantFuImmunizationsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantFuImmunizations, InfantFuImmunizationsAdmin)

from django.contrib import admin

from ..models import InfantFuImmunizations



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

admin.site.register(InfantFuImmunizations, InfantFuImmunizationsAdmin)

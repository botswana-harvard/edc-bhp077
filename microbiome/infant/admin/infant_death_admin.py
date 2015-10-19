from django.contrib import admin


from ..models import InfantDeath


class InfantDeathAdmin(admin.ModelAdmin):

    list_display = ('study_drug_relate', 'infant_nvp_relate', 'haart_relate',)

    list_filter = ('study_drug_relate',)

    radio_fields = {
        'study_drug_relate': admin.VERTICAL,
        'infant_nvp_relate': admin.VERTICAL,
        'haart_relate': admin.VERTICAL,
        'trad_med_relate': admin.VERTICAL
    }

admin.site.register(InfantDeath, InfantDeathAdmin)

from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import InfantBirthArv


class InfantBirthArvAdmin(BaseModelAdmin):

    list_display = ('infant_birth', 'azt_dose_date',)

    list_filter = ('azt_after_birth', 'azt_dose_date', 'azt_additional_dose', 'sdnvp_after_birth',)

    radio_fields = {
        'azt_after_birth': admin.VERTICAL,
        'azt_additional_dose': admin.VERTICAL,
        'sdnvp_after_birth': admin.VERTICAL,
        'additional_nvp_doses': admin.VERTICAL,
        'azt_discharge_supply': admin.VERTICAL,
        'nvp_discharge_supply': admin.VERTICAL,
    }
admin.site.register(InfantBirthArv, InfantBirthArvAdmin)

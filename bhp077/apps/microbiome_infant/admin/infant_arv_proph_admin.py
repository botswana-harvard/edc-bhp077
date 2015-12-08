from django.contrib import admin

from ..models import InfantArvProphMod, InfantArvProph

from .base_infant_scheduled_modeladmin import BaseInfantScheduleModelAdmin


class InfantArvProphAdmin(BaseInfantScheduleModelAdmin):

    radio_fields = {
        'prophylatic_nvp': admin.VERTICAL,
        'arv_status': admin.VERTICAL,
    }

admin.site.register(InfantArvProph, InfantArvProphAdmin)


class InfantArvProphModAdmin(BaseInfantScheduleModelAdmin):

    list_filter = ('infant_arv_proph',)

admin.site.register(InfantArvProphMod, InfantArvProphModAdmin)

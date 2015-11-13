from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import InfantArvProphMod, InfantArvProph


class InfantArvProphAdmin(BaseModelAdmin):

    radio_fields = {
        'prophylatic_nvp': admin.VERTICAL,
        'arv_status': admin.VERTICAL,
    }

admin.site.register(InfantArvProph, InfantArvProphAdmin)


class InfantArvProphModAdmin(BaseModelAdmin):

    list_filter = ('infant_arv_proph',)

admin.site.register(InfantArvProphMod, InfantArvProphModAdmin)

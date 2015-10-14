from django.contrib import admin
from ..models import InfantArvProphMod, InfantArvProph


class InfantArvProphAdmin(admin.ModelAdmin):

    radio_fields = {'prophylatic_nvp': admin.VERTICAL}

admin.site.register(InfantArvProph, InfantArvProphAdmin)


class InfantArvProphModAdmin(admin.ModelAdmin):

    list_filter = ('infant_arv_proph',)

admin.site.register(InfantArvProphMod, InfantArvProphModAdmin)

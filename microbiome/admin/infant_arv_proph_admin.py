from django.contrib import admin
from .site import admin_site
from ..models import InfantArvProphMod, InfantArvProph


class InfantArvProphAdmin(admin.ModelAdmin):

    radio_fields = {'prophylatic_nvp': admin.VERTICAL}

admin_site.register(InfantArvProph, InfantArvProphAdmin)


class InfantArvProphModAdmin(admin.ModelAdmin):

    list_filter = ('infant_arv_proph',)

admin_site.register(InfantArvProphMod, InfantArvProphModAdmin)

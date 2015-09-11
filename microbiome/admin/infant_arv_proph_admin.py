from django.contrib import admin
from .site import admin_site
from ..models import InfantProphMod, InfantProph


class InfantProphAdmin(admin.ModelAdmin):

    radio_fields = {'prophylatic_nvp': admin.VERTICAL}

admin_site.register(InfantProph, InfantProphAdmin)


class InfantProphModAdmin(admin.ModelAdmin):

    list_filter = ('infant_arv_proph',)

admin_site.register(InfantProphMod, InfantProphModAdmin)

from django.contrib import admin

from ..models import InfantFuNewMed

from .site import admin_site


class InfantFuNewMedAdmin(admin.ModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }

admin_site.register(InfantFuNewMed, InfantFuNewMedAdmin)

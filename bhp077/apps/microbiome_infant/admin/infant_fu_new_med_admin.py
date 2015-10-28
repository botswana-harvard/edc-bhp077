from django.contrib import admin

from ..models import InfantFuNewMed


class InfantFuNewMedAdmin(admin.ModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }

admin.site.register(InfantFuNewMed, InfantFuNewMedAdmin)

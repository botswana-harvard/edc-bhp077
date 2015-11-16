from django.contrib import admin

from ..models import InfantFuNewMed

from edc.base.modeladmin.admin import BaseModelAdmin


class InfantFuNewMedAdmin(BaseModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }

admin.site.register(InfantFuNewMed, InfantFuNewMedAdmin)

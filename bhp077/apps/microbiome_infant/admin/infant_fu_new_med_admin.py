from django.contrib import admin

from ..models import InfantFuNewMed

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.base.modeladmin.admin import BaseTabularInline

from .infant_fu_new_med_items_admin import InfantFuNewMedItemsAdmin
from bhp077.apps.microbiome_infant.forms import InfantFuNewMedItemsForm
from bhp077.apps.microbiome_infant.models import InfantFuNewMedItems

class InfantFuNewMedItemsInline(BaseTabularInline):

    model = InfantFuNewMedItems
    form = InfantFuNewMedItemsForm
    extra = 0

class InfantFuNewMedAdmin(BaseModelAdmin):

    radio_fields = {'new_medications': admin.VERTICAL, }

    inlines = [InfantFuNewMedItemsInline, ]

admin.site.register(InfantFuNewMed, InfantFuNewMedAdmin)

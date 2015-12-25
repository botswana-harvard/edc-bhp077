from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline

from ..forms import MaternalPostFuMedForm, MaternalPostFuMedItemsForm
from ..models import MaternalPostFuMed, MaternalPostFuMedItems

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalPostFuMedItemsInlineAdmin(BaseTabularInline):

    model = MaternalPostFuMedItems
    form = MaternalPostFuMedItemsForm
    extra = 1


class MaternalPostFuMedItemsAdmin(BaseMaternalModelAdmin):

    form = MaternalPostFuMedItemsForm

    radio_fields = {
        "medication": admin.VERTICAL,
        "drug_route": admin.VERTICAL,
    }

admin.site.register(MaternalPostFuMedItems, MaternalPostFuMedItemsAdmin)


class MaternalPostFuMedAdmin(BaseMaternalModelAdmin):

    form = MaternalPostFuMedForm

    inlines = [MaternalPostFuMedItemsInlineAdmin, ]

    fields = (
        "maternal_visit",
        "report_datetime",
        "has_taken_meds",
    )

    radio_fields = {
        "has_taken_meds": admin.VERTICAL, }

admin.site.register(MaternalPostFuMed, MaternalPostFuMedAdmin)

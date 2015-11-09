from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import InfantFeedingForm
from ..models import InfantFeeding


class InfantFeedingAdmin(BaseModelAdmin):

    form = InfantFeedingForm
    fields = (
        "infant_visit",
        "report_datetime",
        "last_att_sche_visit",
        "other_feeding",
        "formula_intro_occur",
        "formula_date",
        "formula",
        "water",
        "juice",
        "cow_milk",
        "cow_milk_yes",
        "other_milk",
        "other_milk_animal",
        "milk_boiled",
        "fruits_veg",
        "cereal_porridge",
        "solid_liquid",
        "rehydration_salts",
        "water_used",
        "water_used_other",
        "reason_rcv_formula",
        "reason_rcv_fm_other",
        "ever_breastfeed",
        "complete_weaning",
        "weaned_completely",
        "most_recent_bm",
        "times_breastfed",
        "comments")
    radio_fields = {
        "other_feeding": admin.VERTICAL,
        "formula_intro_occur": admin.VERTICAL,
        "reason_rcv_formula": admin.VERTICAL,
        "water_used": admin.VERTICAL,
        "formula": admin.VERTICAL,
        "water": admin.VERTICAL,
        "juice": admin.VERTICAL,
        "cow_milk": admin.VERTICAL,
        "cow_milk_yes": admin.VERTICAL,
        "other_milk": admin.VERTICAL,
        "milk_boiled": admin.VERTICAL,
        "fruits_veg": admin.VERTICAL,
        "cereal_porridge": admin.VERTICAL,
        "solid_liquid": admin.VERTICAL,
        "rehydration_salts": admin.VERTICAL,
        "ever_breastfeed": admin.VERTICAL,
        "complete_weaning": admin.VERTICAL,
        "weaned_completely": admin.VERTICAL,
        "times_breastfed": admin.VERTICAL}

admin.site.register(InfantFeeding, InfantFeedingAdmin)

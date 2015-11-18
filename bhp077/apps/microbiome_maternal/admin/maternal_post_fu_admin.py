from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalPostFuForm, MaternalPostFuDxForm, MaternalPostFuDxTForm
from ..models import MaternalPostFu, MaternalPostFuDx, MaternalPostFuDxT


class MaternalPostFuAdmin(BaseModelAdmin):

    form = MaternalPostFuForm
    fields = (
        "maternal_visit",
        "mother_weight",
        "enter_weight",
        "bp",
        "had_mastitis",
        "has_chronic_cond",
        "chronic_cond",
        "chronic_cond_other",
        "comment")
    radio_fields = {
        "mother_weight": admin.VERTICAL,
        "had_mastitis": admin.VERTICAL,
        "has_chronic_cond": admin.VERTICAL}
    filter_horizontal = ('chronic_cond',)
admin.site.register(MaternalPostFu, MaternalPostFuAdmin)


class MaternalPostFuDxTInlineAdmin(BaseTabularInline):

    model = MaternalPostFuDxT
    form = MaternalPostFuDxTForm
    extra = 1


class MaternalPostFuDxTAdmin(BaseModelAdmin):
    form = MaternalPostFuDxTForm
    fields = (
        'post_fu_dx',
        'post_fu_specify',
        'grade',
        'hospitalized')
admin.site.register(MaternalPostFuDxT, MaternalPostFuDxTAdmin)


class MaternalPostFuDxAdmin(BaseModelAdmin):

    form = MaternalPostFuDxForm
    fields = (
        "maternal_visit",
        "maternal_post_fu",
        "mother_hospitalized",
        "who_clinical_stage",
        "wcs_dx_adult",
        "new_diagnoses")
    radio_fields = {
        "mother_hospitalized": admin.VERTICAL,
        "new_diagnoses": admin.VERTICAL,
        "who_clinical_stage": admin.VERTICAL}
    filter_horizontal = ("wcs_dx_adult",)
    inlines = [MaternalPostFuDxTInlineAdmin, ]

admin.site.register(MaternalPostFuDx, MaternalPostFuDxAdmin)

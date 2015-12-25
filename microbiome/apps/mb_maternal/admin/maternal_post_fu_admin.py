from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline

from ..forms import MaternalPostFuForm, MaternalPostFuDxForm, MaternalPostFuDxTForm
from ..models import MaternalPostFu, MaternalPostFuDx, MaternalPostFuDxT

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalPostFuAdmin(BaseMaternalModelAdmin):

    form = MaternalPostFuForm
    fields = (
        "maternal_visit",
        "weight_measured",
        "weight_kg",
        "systolic_bp",
        "diastolic_bp",
        "chronic_since",
        "chronic",
        "chronic_other",
        "comment")
    radio_fields = {
        "weight_measured": admin.VERTICAL,
        "chronic_since": admin.VERTICAL}
    filter_horizontal = ('chronic',)

admin.site.register(MaternalPostFu, MaternalPostFuAdmin)


class MaternalPostFuDxTInlineAdmin(BaseTabularInline):

    model = MaternalPostFuDxT
    form = MaternalPostFuDxTForm
    extra = 1


class MaternalPostFuDxTAdmin(BaseMaternalModelAdmin):

    form = MaternalPostFuDxTForm

    fields = (
        'post_fu_dx',
        'post_fu_specify',
        'grade',
        'hospitalized')
    radio_fields = {
        "post_fu_dx": admin.VERTICAL,
        "grade": admin.VERTICAL,
        "hospitalized": admin.VERTICAL,
    }

admin.site.register(MaternalPostFuDxT, MaternalPostFuDxTAdmin)


class MaternalPostFuDxAdmin(BaseMaternalModelAdmin):

    form = MaternalPostFuDxForm

    fields = (
        "maternal_visit",
        "maternal_post_fu",
        "hospitalized_since",
        "new_wcs_dx_since",
        "who",
        "new_dx_since")

    radio_fields = {
        "hospitalized_since": admin.VERTICAL,
        "new_dx_since": admin.VERTICAL,
        "new_wcs_dx_since": admin.VERTICAL}

    filter_horizontal = ("who",)

    inlines = [MaternalPostFuDxTInlineAdmin, ]

admin.site.register(MaternalPostFuDx, MaternalPostFuDxAdmin)

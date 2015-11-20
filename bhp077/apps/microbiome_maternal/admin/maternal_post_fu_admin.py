from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalPostFuForm, MaternalPostFuDxForm, MaternalPostFuDxTForm
from ..models import MaternalPostFu, MaternalPostFuDx, MaternalPostFuDxT, MaternalVisit


class MaternalPostFuAdmin(BaseModelAdmin):

    form = MaternalPostFuForm
    fields = (
        "maternal_visit",
        "mother_weight",
        "enter_weight",
        "systolic_bp",
        "diastolic_bp",
        "has_chronic_cond",
        "chronic_cond",
        "chronic_cond_other",
        "comment")
    radio_fields = {
        "mother_weight": admin.VERTICAL,
        "has_chronic_cond": admin.VERTICAL}
    filter_horizontal = ('chronic_cond',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalPostFuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
    radio_fields = {
        "post_fu_dx": admin.VERTICAL,
        "grade": admin.VERTICAL,
        "hospitalized": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        if db_field.name == "post_fu_dx":
            if request.GET.get('maternal_visit'):
                infant_visit = MaternalVisit.objects.get(id=request.GET.get('maternal_visit'))
                kwargs["queryset"] = MaternalPostFuDxT.objects.filter(registered_subject=infant_visit.appointment.registered_subject)
        return super(MaternalPostFuDxTAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        if db_field.name == "maternal_post_fu":
            if request.GET.get('maternal_visit'):
                infant_visit = MaternalVisit.objects.get(id=request.GET.get('maternal_visit'))
                kwargs["queryset"] = MaternalPostFuDx.objects.filter(registered_subject=infant_visit.appointment.registered_subject)
        return super(MaternalPostFuDxAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuDx, MaternalPostFuDxAdmin)

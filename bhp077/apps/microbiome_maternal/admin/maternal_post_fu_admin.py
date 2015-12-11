from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from edc.export.actions import export_as_csv_action

from ..forms import MaternalPostFuForm, MaternalPostFuDxForm, MaternalPostFuDxTForm
from ..models import MaternalPostFu, MaternalPostFuDx, MaternalPostFuDxT, MaternalVisit


class MaternalPostFuAdmin(BaseModelAdmin):

    form = MaternalPostFuForm
    fields = (
        "maternal_visit",
        "weight_measured",
        "weight_kg",
        "systolic_bp",
        "diastolic_bp",
        "chronic_cond_since",
        "chronic_cond",
        "chronic_cond_other",
        "comment")
    radio_fields = {
        "weight_measured": admin.VERTICAL,
        "chronic_cond_since": admin.VERTICAL}
    filter_horizontal = ('chronic_cond',)

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Postnatal Follow-Up",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'registered': 'maternal_visit__appointment__registered_subject__registration_datetime'}),
        )]

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

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Postnatal Follow-Up: Dx with diagnosis",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 'weight_measured': 'post_fu_dx__weight_measured',
                 'weight_kg': 'post_fu_dx__weight_kg',
                 'systolic_bp': 'post_fu_dx__systolic_bp',
                 'diastolic_bp': 'post_fu_dx__diastolic_bp',
                 'chronic_cond_since': 'post_fu_dx__chronic_cond_since',
                 'chronic_cond': 'post_fu_dx__chronic_cond',
                 'chronic_cond_other': 'post_fu_dx__chronic_cond_other',
                 'comment': 'post_fu_dx__comment'
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_post_fu_dx":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalPostFuDx.objects.filter(
                    maternal_visit__id=request.GET.get('maternal_visit'))
        return super(MaternalPostFuDxTAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuDxT, MaternalPostFuDxTAdmin)


class MaternalPostFuDxAdmin(BaseModelAdmin):

    form = MaternalPostFuDxForm
    fields = (
        "maternal_visit",
        "maternal_post_fu",
        "hospitalized_since",
        "new_wcs_dx_since",
        "wcs_dx_adult",
        "new_dx_since")
    radio_fields = {
        "hospitalized_since": admin.VERTICAL,
        "new_dx_since": admin.VERTICAL,
        "new_wcs_dx_since": admin.VERTICAL}
    filter_horizontal = ("wcs_dx_adult",)
    inlines = [MaternalPostFuDxTInlineAdmin, ]

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Postnatal Follow-Up: Dx",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_visit__appointment__registered_subject__dob',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        if db_field.name == "maternal_post_fu":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalPostFu.objects.filter(maternal_visit__id=request.GET.get('maternal_visit'))
        return super(MaternalPostFuDxAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuDx, MaternalPostFuDxAdmin)

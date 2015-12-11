from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from edc.export.actions import export_as_csv_action

from ..forms import MaternalPostFuMedForm, MaternalPostFuMedItemsForm
from ..models import MaternalPostFuMed, MaternalPostFuMedItems, MaternalVisit


class MaternalPostFuMedItemsInlineAdmin(BaseTabularInline):

    model = MaternalPostFuMedItems
    form = MaternalPostFuMedItemsForm
    extra = 1


class MaternalPostFuMedItemsAdmin(BaseModelAdmin):
    form = MaternalPostFuMedItemsForm

    radio_fields = {
        "medication": admin.VERTICAL,
        "drug_route": admin.VERTICAL,
    }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Postnatal Follow-Up: Medications with meds list",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'maternal_post_fu_med__maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_post_fu_med__maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_post_fu_med__maternal_visit__appointment__registered_subject__dob',
                 'has_taken_meds': 'maternal_post_fu_med__has_taken_meds'
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_post_fu_med":
                kwargs["queryset"] = MaternalPostFuMed.objects.filter(id=request.GET.get('maternal_post_fu_med'))
        return super(MaternalPostFuMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuMedItems, MaternalPostFuMedItemsAdmin)


class MaternalPostFuMedAdmin(BaseModelAdmin):

    form = MaternalPostFuMedForm
    inlines = [MaternalPostFuMedItemsInlineAdmin, ]

    fields = (
        "maternal_visit",
        "report_datetime",
        "has_taken_meds",
    )

    radio_fields = {
        "has_taken_meds": admin.VERTICAL, }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Postnatal Follow-Up: Medications",
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
        return super(MaternalPostFuMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalPostFuMed, MaternalPostFuMedAdmin)

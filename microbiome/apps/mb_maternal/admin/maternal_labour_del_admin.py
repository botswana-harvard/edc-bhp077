from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from edc.export.actions import export_as_csv_action

from ..models import (MaternalLabourDel, MaternalLabDelMed, MaternalLabDelClinic,
                      MaternalLabDelDx, MaternalLabDelDxT, MaternalVisit)
from ..forms import (MaternalLabourDelForm, MaternalLabDelMedForm,
                     MaternalLabDelClinicForm, MaternalLabDelDxForm, MaternalLabDelDxTForm)


class MaternalLabourDelAdmin(BaseModelAdmin):

    form = MaternalLabourDelForm

    list_display = ('delivery_datetime',
                    'labour_hrs',
                    'delivery_hospital',
                    'live_infants_to_register')
    radio_fields = {'delivery_time_estimated': admin.VERTICAL,
                    'has_uterine_tender': admin.VERTICAL,
                    'has_chorioamnionitis': admin.VERTICAL,
                    'delivery_hospital': admin.VERTICAL,
                    'delivery_complications': admin.VERTICAL,
                    'has_temp': admin.VERTICAL, }

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Labour and Delivery",
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
        return super(MaternalLabourDelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabourDel, MaternalLabourDelAdmin)


class MaternalLabDelMedAdmin(BaseModelAdmin):

    form = MaternalLabDelMedForm
    list_display = ('has_health_cond', 'has_ob_comp')
    radio_fields = {'has_health_cond': admin.VERTICAL,
                    'has_ob_comp': admin.VERTICAL,
                    'took_supplements': admin.VERTICAL}
    filter_horizontal = ('supplements', 'health_cond', 'ob_comp')

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Labour & Delivery: Medical History",
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
        return super(MaternalLabDelMedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelMed, MaternalLabDelMedAdmin)


class MaternalLabDelClinicAdmin(BaseModelAdmin):

    form = MaternalLabDelClinicForm
    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Labour & Delivery: Clinical History",
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
        return super(MaternalLabDelClinicAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelClinic, MaternalLabDelClinicAdmin)


class MaternalLabDelDxTInlineAdmin(BaseTabularInline):
    model = MaternalLabDelDxT
    form = MaternalLabDelDxTForm
    extra = 1


class MaternalLabDelDxAdmin(BaseModelAdmin):

    form = MaternalLabDelDxForm
    radio_fields = {'has_preg_dx': admin.VERTICAL,
                    'has_who_dx': admin.VERTICAL}
    filter_horizontal = ('who',)
    inlines = [MaternalLabDelDxTInlineAdmin, ]

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Labour & Delivery: Preg Dx",
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
        return super(MaternalLabDelDxAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalLabDelDx, MaternalLabDelDxAdmin)


class MaternalLabDelDxTAdmin(BaseModelAdmin):

    form = MaternalLabDelDxTForm

    radio_fields = {
        'lab_del_dx': admin.VERTICAL,
        'hospitalized': admin.VERTICAL}
    radio_fields = {'hospitalized': admin.VERTICAL}

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Labour & Delivery: Preg Dx with diagnosis",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier':
                 'maternal_lab_del_dx__maternal_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'maternal_lab_del_dx__maternal_visit__appointment__registered_subject__gender',
                 'dob': 'maternal_lab_del_dx__maternal_visit__appointment__registered_subject__dob',
                 'has_who_dx': 'maternal_lab_del_dx__has_who_dx',
                 'who': 'maternal_lab_del_dx__who',
                 'has_preg_dx': 'maternal_lab_del_dx__has_preg_dx',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalLabDelDxTAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(MaternalLabDelDxT, MaternalLabDelDxTAdmin)

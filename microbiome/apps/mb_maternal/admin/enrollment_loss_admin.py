from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.export.actions import export_as_csv_action

from ..forms import AntenatalEnrollmentLossForm, PostnatalEnrollmentLossForm
from ..models import AntenatalEnrollmentLoss, PostnatalEnrollmentLoss


class AntenatalEnrollmentLossAdmin(BaseModelAdmin):

    form = AntenatalEnrollmentLossForm

    fields = ('antenatal_enrollment',
              'report_datetime',
              'reason_unenrolled')
    list_display = ('antenatal_enrollment',
                    'report_datetime',
                    'reason_unenrolled')
    actions = [
        export_as_csv_action(
            description="CSV Export of Antenatal Enrollment Loss",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'antenatal_enrollment__registered_subject__subject_identifier',
                 'report_datetime': 'report_datetime',
                 'reason_unenrolled': 'reason_unenrolled',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "antenatal_enrollment":
            if request.GET.get('antenatal_enrollment'):
                kwargs["queryset"] = AntenatalEnrollmentLoss.objects.filter(
                    antenatal_enrollment=request.GET.get('antenatal_enrollment'))
        return super(AntenatalEnrollmentLossAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(AntenatalEnrollmentLoss, AntenatalEnrollmentLossAdmin)


class PostnatalEnrollmentLossAdmin(BaseModelAdmin):

    form = PostnatalEnrollmentLossForm

    fields = ('postnatal_enrollment',
              'report_datetime',
              'reason_unenrolled')

    list_display = ('postnatal_enrollment',
                    'report_datetime',
                    'reason_unenrolled')

    actions = [
        export_as_csv_action(
            description="CSV Export of Postnatal Enrollment Loss",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'postnatal_enrollment__registered_subject__subject_identifier',
                 'report_datetime': 'report_datetime',
                 'reason_unenrolled': 'reason_unenrolled',
                 }),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "postnatal_enrollment":
            if request.GET.get('postnatal_enrollment'):
                kwargs["queryset"] = PostnatalEnrollmentLoss.objects.filter(
                    postnatal_enrollment=request.GET.get('postnatal_enrollment'))
        return super(PostnatalEnrollmentLossAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

admin.site.register(PostnatalEnrollmentLoss, PostnatalEnrollmentLossAdmin)

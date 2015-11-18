from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import InfantBirthExam, InfantBirth


class InfantBirthExamAdmin(BaseModelAdmin):

    list_display = (
        'infant_birth',
        'gender',
        'general_activity',
        'physical_exam_result',
        'resp_exam',
    )

    list_filter = (
        'gender',
        'general_activity',
        'abnormal_activity',
        'physical_exam_result',
    )

    radio_fields = {
        'gender': admin.VERTICAL,
        'general_activity': admin.VERTICAL,
        'physical_exam_result': admin.VERTICAL,
        'heent_exam': admin.VERTICAL,
        'resp_exam': admin.VERTICAL,
        'cardiac_exam': admin.VERTICAL,
        'abdominal_exam': admin.VERTICAL,
        'neurologic_exam': admin.VERTICAL
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_lab_del":
            if request.GET.get('infant_birth'):
                maternal_subject_identifier = InfantBirth.objects.get(id=request.GET.get('infant_birth')).relative_identifier
                kwargs["queryset"] = InfantBirth.objects.filter(maternal_visit__appointment__registered_subject__subject_identifier=maternal_subject_identifier)
            else:
                kwargs["queryset"] = InfantBirth.objects.none()

        return super(InfantBirthExamAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantBirthExam, InfantBirthExamAdmin)

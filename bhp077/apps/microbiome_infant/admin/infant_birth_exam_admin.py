from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import InfantBirthExam


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
admin.site.register(InfantBirthExam, InfantBirthExamAdmin)

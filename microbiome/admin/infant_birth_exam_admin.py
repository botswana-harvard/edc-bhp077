from django.contrib import admin

from ..models import InfantBirthExam


@admin.register(InfantBirthExam)
class InfantBirthExamAdmin(admin.ModelAdmin):

    list_display = (
        'infant_birth',
        'gender', 'general_activity',
        'physical_exam_result',
        'resp_exam'
    )

    list_filter = (
        'gender',
        'general_activity',
        'abnormal_activity',
        'physical_exam_result'
    )

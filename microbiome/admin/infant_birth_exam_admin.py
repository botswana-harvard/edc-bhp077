from django.contrib import admin

from .site import admin_site

from ..models import InfantBirthExam


class InfantBirthExamAdmin(admin.ModelAdmin):

    list_display = (
        'infant_birth',
        'gender', 'general_activity',
        'physical_exam_result',
        'resp_exam',
    )

    list_filter = (
        'gender',
        'general_activity',
        'abnormal_activity',
        'physical_exam_result',
    )
admin_site.register(InfantBirthExam, InfantBirthExamAdmin)

from django.contrib import admin

from ..models import InfantOffStudy


@admin.register(InfantOffStudy)
class InfantOffStudyAdmin(admin.ModelAdmin):

    list_display = (
        'infant_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'has_scheduled_data'
    )

    list_filter = ('report_datetime', 'offstudy_date')

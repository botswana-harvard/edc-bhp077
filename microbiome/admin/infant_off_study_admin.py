from django.contrib import admin

from .site import admin_site

from ..models import InfantOffStudy


class InfantOffStudyAdmin(admin.ModelAdmin):

    list_display = (
        'infant_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'has_scheduled_data'
    )

    list_filter = ('report_datetime', 'offstudy_date')

    radio_fields = {'has_scheduled_data': admin.VERTICAL}

admin_site.register(InfantOffStudy, InfantOffStudyAdmin)

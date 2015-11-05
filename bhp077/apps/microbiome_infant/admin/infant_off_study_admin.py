from django.contrib import admin

from ..models import InfantOffStudy


class InfantOffStudyAdmin(admin.ModelAdmin):

    list_display = (
        'infant_visit',
        'offstudy_date',
        'reason',
        'has_scheduled_data'
    )

    radio_fields = {'has_scheduled_data': admin.VERTICAL}

admin.site.register(InfantOffStudy, InfantOffStudyAdmin)

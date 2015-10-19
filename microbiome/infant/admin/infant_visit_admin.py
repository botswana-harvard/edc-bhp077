from django.contrib import admin

from ..models import InfantVisit


class InfantVisitAdmin(admin.ModelAdmin):

    list_display = ('information_provider', 'information_provider_other', 'study_status')

    radio_fields = {
        'information_provider': admin.VERTICAL,
        'study_status': admin.VERTICAL,
        'survival_status': admin.VERTICAL}

admin.site.register(InfantVisit, InfantVisitAdmin)

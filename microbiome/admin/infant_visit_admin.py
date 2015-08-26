from django.contrib import admin

from .site import admin_site

from ..models import InfantVisit


@admin.register(InfantVisit)
class InfantVisitAdmin(admin.ModelAdmin):

    list_display = ('information_provider', 'information_provider_other', 'study_status')

    radio_fields = {
        'information_provider': admin.VERTICAL,
        'study_status': admin.VERTICAL,
        'survival_status': admin.VERTICAL
        }

admin_site.register(InfantVisit, InfantVisitAdmin)

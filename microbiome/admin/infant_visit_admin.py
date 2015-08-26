from django.contrib import admin

from .site import admin_site

from ..models import InfantVisit


@admin.register(InfantVisit)
class InfantVisitAdmin(admin.ModelAdmin):

    list_display = ('information_provider', 'information_provider_other', 'study_status')

admin_site.register(InfantVisit, InfantVisitAdmin)

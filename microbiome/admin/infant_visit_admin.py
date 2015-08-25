from django.contrib import admin

from ..models import InfantVisit


@admin.register(InfantVisit)
class InfantVisitAdmin(admin.ModelAdmin):

    list_display = ('information_provider', 'information_provider_other', 'study_status')

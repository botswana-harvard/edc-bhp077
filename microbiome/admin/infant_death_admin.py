from django.contrib import admin

from ..models import InfantDeath


@admin.register(InfantDeath)
class InfantDeathAdmin(admin.ModelAdmin):

    list_display = ('study_drug_relate', 'infant_nvp_relate', 'haart_relate',)

    list_filter = ('study_drug_relate',)

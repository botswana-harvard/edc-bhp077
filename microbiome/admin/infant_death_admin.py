from django.contrib import admin

from .site import admin_site

from ..models import InfantDeath


class InfantDeathAdmin(admin.ModelAdmin):

    list_display = ('study_drug_relate', 'infant_nvp_relate', 'haart_relate',)

    list_filter = ('study_drug_relate',)

admin_site.register(InfantDeath, InfantDeathAdmin)

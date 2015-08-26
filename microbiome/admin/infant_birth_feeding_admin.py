from django.contrib import admin

from .site import admin_site

from ..models import InfantBirthFeedVaccine


class InfantBirthFeedVaccineAdmin(admin.ModelAdmin):

    list_display = ('infant_birth', 'feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}
admin_site.register(InfantBirthFeedVaccine, InfantBirthFeedVaccineAdmin)

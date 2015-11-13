from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import InfantBirthFeedVaccine


class InfantBirthFeedVaccineAdmin(BaseModelAdmin):

    list_display = ('infant_birth', 'feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    filter_horizontal = ('vaccination', )

    radio_fields = {'feeding_after_delivery': admin.VERTICAL}
admin.site.register(InfantBirthFeedVaccine, InfantBirthFeedVaccineAdmin)

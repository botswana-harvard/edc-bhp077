from django.contrib import admin

from ..models import InfantBirthFeedVaccine


@admin.register(InfantBirthFeedVaccine)
class InfantBirthFeedVaccineAdmin():

    list_display = ('infant_birth', 'feeding_after_delivery')

    list_filter = ('feeding_after_delivery')
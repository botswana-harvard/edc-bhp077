from django.contrib import admin

from ..models import InfantBirth


@admin.register(InfantBirth)
class InfantBirthAdmin(admin.ModelAdmin):

    list_display = (
        'maternal_labour_del',
        'first_name',
        'initials',
        'birth_order',
        'dob',
        'gender',
    )

    list_filter = ('gender',)

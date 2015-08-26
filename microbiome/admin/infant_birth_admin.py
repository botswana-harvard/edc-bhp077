from django.contrib import admin
from .site import admin_site
from ..models import InfantBirth


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
admin_site.register(InfantBirth, InfantBirthAdmin)

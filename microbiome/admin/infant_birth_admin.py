from django.contrib import admin
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

    radio_fields = {'gender': admin.VERTICAL}
admin.register(InfantBirth, InfantBirthAdmin)

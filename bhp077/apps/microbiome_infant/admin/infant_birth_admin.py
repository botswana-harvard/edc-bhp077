from django.contrib import admin
from ..models import InfantBirth


class InfantBirthAdmin(admin.ModelAdmin):

    list_display = (
        'registered_subject',
        'maternal_labour_del',
        'report_datetime',
        'first_name',
        'initials',
        'birth_order',
        'dob',
        'gender',
    )

    list_display = ('report_datetime', 'maternal_labour_del')
    list_filter = ('gender',)
    radio_fields = {'gender': admin.VERTICAL}
admin.site.register(InfantBirth, InfantBirthAdmin)

from django.contrib import admin

from ..models import InfantBirthArv


@admin.register(InfantBirthArv)
class InfantBirthArvAdmin(admin.ModelAdmin):

    list_display = ('infant_birth', 'azt_dose_date', )

    list_filter = ('azt_after_birth', 'azt_dose_date', 'azt_additional_dose', 'sdnvp_after_birth')



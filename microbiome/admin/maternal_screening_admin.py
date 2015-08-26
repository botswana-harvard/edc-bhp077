from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalScreeningForm
from ..models import MaternalScreening
from .site import admin_site


@admin.register(MaternalScreening)
class MaternalScreeningAdmin(BaseModelAdmin):
    form = MaternalScreeningForm

    fields = ('report_datetime',
              'gender',
              'age_in_years',
              'screening_identifier', )
    readonly_fields = ('screening_identifier',)
admin_site.register(MaternalScreening, MaternalScreeningAdmin)

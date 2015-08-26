from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalEligibilityPreForm
from ..models import MaternalEligibilityPre
from .site import admin_site


@admin.register(MaternalEligibilityPre)
class MaternalEligibilityPreAdmin(BaseModelAdmin):
    form = MaternalEligibilityPreForm

    fields = ('report_datetime',
              'gender',
              'age_in_years'
              'screening_identifier' )
    readonly_fields = ('screening_identifier',)
admin_site.register(MaternalEligibilityPre, MaternalEligibilityPreAdmin)

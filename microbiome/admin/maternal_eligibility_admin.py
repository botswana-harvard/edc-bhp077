from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility

from .site import admin_site


class MaternalEligibilityAdmin(BaseModelAdmin):

    form = MaternalEligibilityForm

    fields = ('registered_subject',
              'report_datetime',
              'age_in_years',
              'citizen',
              'is_diabetic',
              'has_tb',
              'breastfeed_for_a_year',
              'instudy_for_a_year',
              'currently_pregnant')
    radio_fields = {'citizen': admin.VERTICAL,
                    'is_diabetic': admin.VERTICAL,
                    'has_tb': admin.VERTICAL,
                    'breastfeed_for_a_year': admin.VERTICAL,
                    'instudy_for_a_year': admin.VERTICAL,
                    'currently_pregnant': admin.VERTICAL}
admin_site.register(MaternalEligibility, MaternalEligibilityAdmin)

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility


class MaternalEligibilityAdmin(BaseModelAdmin):

    form = MaternalEligibilityForm

    fields = ('eligibility_id',
              'report_datetime',
              'age_in_years',
              'has_omang',
              'currently_pregnant',
              'recently_delivered')
    radio_fields = {'currently_pregnant': admin.VERTICAL,
                    'recently_delivered': admin.VERTICAL,
                    'has_omang': admin.VERTICAL}

    readonly_fields = ('eligibility_id',)
    list_display = ('report_datetime', 'age_in_years', 'is_eligible',
                    'is_consented', 'currently_pregnant', 'recently_delivered')
    list_filter = ('report_datetime', 'is_eligible', 'is_consented',
                   'currently_pregnant', 'recently_delivered')
admin.site.register(MaternalEligibility, MaternalEligibilityAdmin)

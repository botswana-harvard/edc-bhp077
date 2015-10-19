from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalEligibilityForm
from ..models import MaternalEligibility


class MaternalEligibilityAdmin(BaseModelAdmin):

    form = MaternalEligibilityForm

    fields = ('eligibility_id',
              'report_datetime',
              'age_in_years',
              # 'ineligibility',
              'currently_pregnant')
    radio_fields = {'currently_pregnant': admin.VERTICAL}
    readonly_fields = ('eligibility_id',)
admin.site.register(MaternalEligibility, MaternalEligibilityAdmin)

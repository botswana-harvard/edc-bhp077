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
              'currently_pregnant')
    radio_fields = {'currently_pregnant': admin.VERTICAL}
admin_site.register(MaternalEligibility, MaternalEligibilityAdmin)

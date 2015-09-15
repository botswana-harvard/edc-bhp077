from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalEligibilityLossForm
from ..models import MaternalEligibilityLoss

from .site import admin_site


class MaternalEligibilityLossAdmin(BaseModelAdmin):

    form = MaternalEligibilityLossForm

    fields = ('maternal_eligibility',
              'report_datetime',
              'reason_ineligible')
admin_site.register(MaternalEligibilityLoss, MaternalEligibilityLossAdmin)

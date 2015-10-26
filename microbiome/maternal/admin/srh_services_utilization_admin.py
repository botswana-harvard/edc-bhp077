from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from microbiome.maternal.models import SrhServicesUtilization
from microbiome.maternal.forms import SrhServicesUtilizationForm


class SrhServicesUtilizationAdmin(BaseModelAdmin):

    form = SrhServicesUtilizationForm

    fields = ('seen_at_clinic',
              'reason_unseen_clinic',
              'reason_unseen_clinic_other',
              'is_contraceptive_initiated',
              'contraceptive_methods',
              'reason_not_initiated',
              'srh_referral',
              'srh_referral_other')
    radio_fields = {'seen_at_clinic': admin.VERTICAL,
                    'reason_unseen_clinic': admin.VERTICAL,
                    'is_contraceptive_initiated': admin.VERTICAL,
                    'reason_not_initiated': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptive_methods',)

admin.site.register(SrhServicesUtilization, SrhServicesUtilizationAdmin)

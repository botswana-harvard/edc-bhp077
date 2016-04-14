from django.contrib import admin

from ..models import ReproductiveHealth
from ..forms import ReproductiveHealthForm

from .base_maternal_model_admin import BaseMaternalModelAdmin


class ReproductiveHealthAdmin(BaseMaternalModelAdmin):

    form = ReproductiveHealthForm

    fields = ('more_children',
              'next_child',
              'contraceptive_measure',
              'contraceptive_partner',
              'contraceptive_relative',
              'contraceptive_relative_other',
              'influential_decision_making',
              'influential_decision_making_other',
              'uses_contraceptive',
              'contr',
              'contr_other',
              'pap_smear',
              'pap_smear_date',
              'pap_smear_estimate',
              'pap_smear_result',
              'pap_smear_result_status',
              'pap_smear_result_abnormal',
              'date_notified',
              'srh_referral')
    radio_fields = {'more_children': admin.VERTICAL,
                    'next_child': admin.VERTICAL,
                    'contraceptive_measure': admin.VERTICAL,
                    'contraceptive_partner': admin.VERTICAL,
                    'influential_decision_making': admin.VERTICAL,
                    'uses_contraceptive': admin.VERTICAL,
                    'pap_smear_estimate': admin.VERTICAL,
                    'pap_smear_result': admin.VERTICAL,
                    'pap_smear_result_status': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptive_relative', 'contr',)

admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)

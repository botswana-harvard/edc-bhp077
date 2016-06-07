from django.contrib import admin

from ..models import ReproductiveHealth
from ..forms import ReproductiveHealthForm

from .base_maternal_model_admin import BaseMaternalModelAdmin


class ReproductiveHealthAdmin(BaseMaternalModelAdmin):

    form = ReproductiveHealthForm

    radio_fields = {'more_children': admin.VERTICAL,
                    'next_child': admin.VERTICAL,
                    'contraceptive_measure': admin.VERTICAL,
                    'contraceptive_partner': admin.VERTICAL,
                    'influential_decision_making': admin.VERTICAL,
                    'uses_contraceptive': admin.VERTICAL,
                    'pap_smear': admin.VERTICAL,
                    'pap_smear_estimate': admin.VERTICAL,
                    'pap_smear_result': admin.VERTICAL,
                    'pap_smear_result_status': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptive_relative', 'contr',)

admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)

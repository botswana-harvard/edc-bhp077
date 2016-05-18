from django.contrib import admin

from ..forms import MaternalSrhForm
from ..models import MaternalSrh

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalSrhAdmin(BaseMaternalModelAdmin):

    form = MaternalSrhForm

#     fields = ('seen_at_clinic',
#               'reason_unseen_clinic',
#               'reason_unseen_clinic_other',
#               'is_contraceptive_initiated',
#               'contr',  # contraceptives
#               'contr_other',
#               'reason_not_initiated',
#               'srh_referral',
#               'srh_referral_other')
    radio_fields = {'seen_at_clinic': admin.VERTICAL,
                    'reason_unseen_clinic': admin.VERTICAL,
                    'is_contraceptive_initiated': admin.VERTICAL,
                    'reason_not_initiated': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contr',)

admin.site.register(MaternalSrh, MaternalSrhAdmin)

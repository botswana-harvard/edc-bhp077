from django.contrib import admin

from ..models import ReproductiveHealth
from ..forms import ReproductiveHealthForm

from .base_maternal_model_admin import BaseMaternalModelAdmin


class ReproductiveHealthAdmin(BaseMaternalModelAdmin):

    form = ReproductiveHealthForm

    fields = ('more_children',
              'next_child',
              'contraceptive_measure',
              'uses_contraceptive',
              'contr',
              'contr_other',
              'srh_referral')
    radio_fields = {'more_children': admin.VERTICAL,
                    'next_child': admin.VERTICAL,
                    'contraceptive_measure': admin.VERTICAL,
                    'uses_contraceptive': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contr',)

admin.site.register(ReproductiveHealth, ReproductiveHealthAdmin)

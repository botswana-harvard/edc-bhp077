from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..models import SexualReproductiveHealth
from ..forms import SexualReproductiveHealthForm


class SexualReproductiveHealthAdmin(BaseModelAdmin):

    form = SexualReproductiveHealthForm

    fields = ('more_children',
              'next_child',
              'contraceptive_measure',
              'uses_contraceptive',
              'contraceptives_used',
              'contraceptives_used_other',
              'srh_referral')
    radio_fields = {'more_children': admin.VERTICAL,
                    'next_child': admin.VERTICAL,
                    'contraceptive_measure': admin.VERTICAL,
                    'uses_contraceptive': admin.VERTICAL,
                    'srh_referral': admin.VERTICAL}
    filter_horizontal = ('contraceptives_used',)

admin.site.register(SexualReproductiveHealth, SexualReproductiveHealthAdmin)

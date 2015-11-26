from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalHeightWeightForm
from ..models import MaternalHeightWeight


class MaternalHeightWeightAdmin(BaseModelAdmin):

    form = MaternalHeightWeightForm
    fields = ('weight',
              'height',
              'systolic_bp',
              'diastolic_bp')
admin.site.register(MaternalHeightWeight, MaternalHeightWeightAdmin)

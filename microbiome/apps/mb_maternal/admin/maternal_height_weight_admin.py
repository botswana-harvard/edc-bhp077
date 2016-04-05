from django.contrib import admin

from ..forms import MaternalHeightWeightForm
from ..models import MaternalHeightWeight

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalHeightWeightAdmin(BaseMaternalModelAdmin):

    form = MaternalHeightWeightForm

    fields = ('maternal_visit',
              'weight_kg',
              'height',
              'systolic_bp',
              'diastolic_bp')

admin.site.register(MaternalHeightWeight, MaternalHeightWeightAdmin)

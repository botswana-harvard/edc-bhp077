from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalUninfectedForm
from ..models import MaternalUninfected


class MaternalUninfectedAdmin(BaseModelAdmin):

    form = MaternalUninfectedForm
    fields = ('prev_pregnancies',
              'weight',
              'height',
              'systolic_bp',
              'diastolic_bp')
admin.site.register(MaternalUninfected, MaternalUninfectedAdmin)

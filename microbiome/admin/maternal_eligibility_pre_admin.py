from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalEligibilityPreForm
from ..models import MaternalEligibilityPre
from .site import admin_site


@admin.register(MaternalEligibilityPre)
class MaternalEligibilityPreAdmin(BaseModelAdmin):
    form = MaternalEligibilityPreForm

    fields = ('report_datetime',
              'first_name',
              'initials',
              'dob',
              'gender',
              'has_identity',
              'citizen',
              'disease',
              'currently_pregnant',
              'pregnancy_weeks',
              'verbal_hiv_status',
              'evidence_pos_hiv_status',
              'rapid_test_result', )
    radio_fields = {'gender':admin.VERTICAL,
                    'has_identity':admin.VERTICAL,
                    'citizen':admin.VERTICAL,
                    'disease':admin.VERTICAL,
                    'currently_pregnant':admin.VERTICAL,
                    'verbal_hiv_status':admin.VERTICAL,
                    'rapid_test_result':admin.VERTICAL, }
admin_site.register(MaternalEligibilityPre, MaternalEligibilityPreAdmin)

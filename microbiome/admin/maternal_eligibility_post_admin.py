from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalEligibilityPostForm
from ..models import MaternalEligibilityPost
from .site import admin_site


class MaternalEligibilityPostAdmin(BaseModelAdmin):
    form = MaternalEligibilityPostForm
    fields = ('registered_subject',
              'report_datetime',
              'disease',
              'currently_pregnant',
              'weeks_of_gestation',
              'days_post_natal',
              'type_of_birth',
              'live_infants',
              'verbal_hiv_status',
              'evidence_pos_hiv_status',
              'rapid_test_result',
              'rapid_test_result_datetime',
              'haart_during_preg',
              'haart_start_date',
              'drug_during_preg',
              'enrollment_status')
    radio_fields = {'type_of_birth': admin.VERTICAL, }
admin_site.register(MaternalEligibilityPost, MaternalEligibilityPostAdmin)

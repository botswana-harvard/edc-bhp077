from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalEligibilityPostForm
from ..models import MaternalEligibilityPost
from .site import admin_site


class MaternalEligibilityPostAdmin(BaseModelAdmin):
    form = MaternalEligibilityPostForm
    fields = ('registered_subject',
              'report_datetime', 
              'days_post_natal',
              'weeks_of_gestation',
              'type_of_birth',
              'live_infants', )
    radio_fields = {'type_of_birth':admin.VERTICAL, }
admin_site.register(MaternalEligibilityPost, MaternalEligibilityPostAdmin)

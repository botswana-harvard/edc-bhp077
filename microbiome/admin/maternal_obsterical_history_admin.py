from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalObstericalHistoryForm
from ..models import MaternalObstericalHistory
from .site import admin_site


class MaternalObstericalHistoryAdmin(BaseModelAdmin):

    form = MaternalObstericalHistoryForm
    fields = ('pregs_24wks_or_more',
              'lost_before_24wks',
              'lost_after_24wks',
              'live_children',
              'children_died_b4_5yrs')
    list_display = ('pregs_24wks_or_more',
                    'lost_before_24wks',
                    'lost_after_24wks',
                    'live_children')
admin_site.register(MaternalObstericalHistory, MaternalObstericalHistoryAdmin)

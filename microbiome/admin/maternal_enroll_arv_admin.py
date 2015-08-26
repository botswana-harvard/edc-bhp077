from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..models import MaternalEnrollArv
from ..forms import MaternalEnrollArvForm
from .site import admin_site


class MaternalEnrollArvAdmin(BaseModelAdmin):
    form = MaternalEnrollArvForm
    
    list_display = ('haart_start_date', 'preg_on_haart')
    list_filter = ('preg_on_haart', )
    radio_fields = {'preg_on_haart':admin.VERTICAL,
                    'prior_preg':admin.VERTICAL, }
    filter_horizontal = ('prior_arv', )
admin_site.register(MaternalEnrollArv, MaternalEnrollArvAdmin)

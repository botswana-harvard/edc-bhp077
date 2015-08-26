from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from .site import admin_site
from ..models import MaternalLocator


class MaternalLocatorAdmin(BaseModelAdmin):
    list_display = ('maternal_visit',
                    'care_clinic',
                    'caretaker_name',
                    'caretaker_cell',
                    'caretaker_tel')
    list_filter = ('care_clinic', )
    search_fields = ('care_clinic', )
    radio_fields = {'has_caretaker_alt':admin.VERTICAL, }
admin_site.register(MaternalLocator, MaternalLocatorAdmin)

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from .site import admin_site
from ..models import MaternalVisit


class MaternalVisitAdmin(BaseModelAdmin):
    pass
admin_site.register(MaternalVisit, MaternalVisitAdmin)

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..models import MaternalVisit


class MaternalVisitAdmin(BaseModelAdmin):
    pass
admin.site.register(MaternalVisit, MaternalVisitAdmin)

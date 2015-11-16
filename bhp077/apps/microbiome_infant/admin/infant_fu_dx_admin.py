from django.contrib import admin

from ..models import InfantFuDx
from edc.base.modeladmin.admin import BaseModelAdmin


class InfantFuDxAdmin(BaseModelAdmin):
    pass
admin.site.register(InfantFuDx, InfantFuDxAdmin)

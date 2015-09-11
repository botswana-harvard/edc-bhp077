from django.contrib import admin

from ..models import InfantFuDx

from .site import admin_site


class InfantFuDxAdmin(admin.ModelAdmin):
    pass
admin_site.register(InfantFuDx, InfantFuDxAdmin)

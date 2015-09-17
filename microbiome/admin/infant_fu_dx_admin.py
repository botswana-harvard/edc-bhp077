from django.contrib import admin

from ..models import InfantFuDx


class InfantFuDxAdmin(admin.ModelAdmin):
    pass
admin.site.register(InfantFuDx, InfantFuDxAdmin)

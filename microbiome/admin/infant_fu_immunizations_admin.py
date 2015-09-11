from django.contrib import admin

from ..models import InfantFuImmunizations

from .site import admin_site


class InfantFuImmunizationsAdmin(admin.ModelAdmin):

    list_display = ('vaccines_received', )

    radio_fields = {'vaccines_received': admin.VERTICAL, }
admin_site.register(InfantFuImmunizations, InfantFuImmunizationsAdmin)

from django.contrib import admin
from .site import admin_site
from ..models import InfantCircumcision


class InfantCircumcisionAdmin(admin.ModelAdmin):

    list_filter = ('circumcised',)

    radio_fields = {'circumcised': admin.VERTICAL}
admin_site.register(InfantCircumcision, InfantCircumcisionAdmin)

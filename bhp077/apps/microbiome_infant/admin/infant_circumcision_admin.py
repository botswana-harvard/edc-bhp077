from django.contrib import admin
from ..models import InfantCircumcision

from edc.base.modeladmin.admin import BaseModelAdmin


class InfantCircumcisionAdmin(BaseModelAdmin):

    list_filter = ('circumcised',)

    radio_fields = {'circumcised': admin.VERTICAL}
admin.site.register(InfantCircumcision, InfantCircumcisionAdmin)

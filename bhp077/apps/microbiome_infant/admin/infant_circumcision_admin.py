from django.contrib import admin
from ..models import InfantCircumcision


class InfantCircumcisionAdmin(admin.ModelAdmin):

    list_filter = ('circumcised',)

    radio_fields = {'circumcised': admin.VERTICAL}
admin.site.register(InfantCircumcision, InfantCircumcisionAdmin)

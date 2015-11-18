from django.contrib import admin
from ..models import InfantCircumcision

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import InfantVisit


class InfantCircumcisionAdmin(BaseModelAdmin):

    list_filter = ('circumcised',)

    radio_fields = {'circumcised': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "infant_visit":
                kwargs["queryset"] = InfantVisit.objects.filter(id=request.GET.get('infant_visit'))
        return super(InfantCircumcisionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantCircumcision, InfantCircumcisionAdmin)

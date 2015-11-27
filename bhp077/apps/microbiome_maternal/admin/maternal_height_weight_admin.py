from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalHeightWeightForm
from ..models import MaternalHeightWeight, MaternalVisit


class MaternalHeightWeightAdmin(BaseModelAdmin):

    form = MaternalHeightWeightForm
    fields = ('maternal_visit',
              'weight',
              'height',
              'systolic_bp',
              'diastolic_bp')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalHeightWeightAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(MaternalHeightWeight, MaternalHeightWeightAdmin)

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import MaternalEligibilityLossForm
from ..models import MaternalEligibilityLoss, MaternalEligibility


class MaternalEligibilityLossAdmin(BaseModelAdmin):

    form = MaternalEligibilityLossForm

    fields = ('maternal_eligibility',
              'report_datetime',
              'reason_ineligible')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_eligibility":
            if request.GET.get('maternal_eligibility'):
                kwargs["queryset"] = MaternalEligibility.objects.filter(id=request.GET.get('maternal_eligibility'))
        return super(MaternalEligibilityLossAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalEligibilityLoss, MaternalEligibilityLossAdmin)

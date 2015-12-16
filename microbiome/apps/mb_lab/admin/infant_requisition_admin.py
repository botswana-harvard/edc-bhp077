from django.contrib import admin

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin

from microbiome.apps.mb_infant.models import InfantVisit

from ..forms import InfantRequisitionForm
from ..models import InfantRequisition, Panel


class InfantRequisitionAdmin(BaseRequisitionModelAdmin):

    form = InfantRequisitionForm
    visit_model = InfantVisit
    visit_attr = 'infant_visit'
    dashboard_type = 'infant'

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionAdmin, self).__init__(*args, **kwargs)
        for fld in ['test_code']:
            self.fields.remove(fld)

    def get_fieldsets(self, request, obj=None):
        panel = Panel.objects.get(id=request.GET.get('panel'))
        if panel.name in ['Rectal swab (Storage)']:
            for field in ['estimated_volume']:
                if field in self.fields:
                    self.fields.remove(field)
        return [(None, {'fields': self.fields})]

admin.site.register(InfantRequisition, InfantRequisitionAdmin)

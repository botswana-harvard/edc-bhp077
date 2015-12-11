from django.contrib import admin

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin

from bhp077.apps.microbiome_infant.models import InfantVisit
from ..models import InfantRequisition
from ..forms import InfantRequisitionForm
from bhp077.apps.microbiome_lab.models.panel import Panel


class InfantRequisitionAdmin(BaseRequisitionModelAdmin):

    form = InfantRequisitionForm
    visit_model = InfantVisit
#     visit_fieldname = 'infant_visit'
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

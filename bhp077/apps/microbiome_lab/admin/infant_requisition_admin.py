from django.contrib import admin

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin

from bhp077.apps.microbiome_infant.models import InfantVisit
from ..models import InfantRequisition
from ..forms import InfantRequisitionForm


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

admin.site.register(InfantRequisition, InfantRequisitionAdmin)

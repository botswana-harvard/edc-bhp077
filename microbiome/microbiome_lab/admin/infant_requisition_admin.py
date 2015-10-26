from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin

from microbiome.infant.models import InfantVisit


class InfantRequisitionAdmin(BaseRequisitionModelAdmin):

    visit_model = InfantVisit
    visit_fieldname = 'infant_visit'
    dashboard_type = 'infant'

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionAdmin, self).__init__(*args, **kwargs)
        for fld in ['test_code']:
            self.fields.remove(fld)

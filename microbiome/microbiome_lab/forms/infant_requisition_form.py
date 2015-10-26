from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import InfantRequisition


class InfantRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    class Meta:
        model = InfantRequisition
